"""
PDF Processing Service
Handles PDF text extraction, detection, and redaction
"""
import fitz  # PyMuPDF
import io
from typing import List, Dict, Set, Optional
from app.services.redaction_patterns import RedactionPatterns
from app.services.header_footer_service import HeaderFooterService, DefaultHeaderFooter
from app.services.docx_service import DOCXService


class PDFProcessor:
    """
    Main PDF processing class for redaction operations
    """

    def __init__(self, pdf_bytes: bytes):
        """
        Initialize PDF processor with PDF file bytes

        Args:
            pdf_bytes: PDF file as bytes
        """
        self.pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        self.redaction_patterns = RedactionPatterns()

    def extract_text(self) -> str:
        """Extract all text from the PDF"""
        text = ""
        for page in self.pdf_document:
            text += page.get_text()
        return text

    def find_sensitive_data(self, redaction_types: List[str]) -> Dict:
        """
        Find all sensitive data in the PDF

        Args:
            redaction_types: List of data types to find (email, phone, linkedin, portfolio)

        Returns:
            Dictionary with found sensitive data
        """
        full_text = self.extract_text()
        return self.redaction_patterns.get_redaction_items(full_text, redaction_types)

    def search_and_redact(self, search_terms: Set[str], redaction_color: tuple = (0, 0, 0)):
        """
        Search for specific terms in PDF and redact them

        Args:
            search_terms: Set of terms to search and redact
            redaction_color: RGB color tuple for redaction boxes
        """
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document[page_num]

            for term in search_terms:
                # Search for the term (case insensitive)
                text_instances = page.search_for(term)

                # Add redaction annotation for each instance
                for inst in text_instances:
                    # Create a redaction annotation
                    redact_annot = page.add_redact_annot(inst, fill=redaction_color)

            # Apply all redactions on this page
            page.apply_redactions()

    def add_header_footer(self, header_config: Optional[Dict] = None,
                         footer_config: Optional[Dict] = None,
                         logo_bytes: Optional[bytes] = None):
        """
        Add header and footer to PDF

        Args:
            header_config: Header configuration dictionary
            footer_config: Footer configuration dictionary
            logo_bytes: Logo image bytes
        """
        hf_service = HeaderFooterService(self.pdf_document)

        # Prepare header config with logo
        if header_config and logo_bytes:
            header_config['logo_bytes'] = logo_bytes

        hf_service.add_header_footer(header_config, footer_config)

    def redact_pdf(self, redaction_types: List[str], output_format: str = 'pdf',
                   header_config: Optional[Dict] = None,
                   footer_config: Optional[Dict] = None,
                   logo_bytes: Optional[bytes] = None) -> bytes:
        """
        Main method to redact PDF based on specified types

        Args:
            redaction_types: List of data types to redact (email, phone, linkedin, portfolio, all_urls)
            output_format: Output format (pdf, or could extend to support images)
            header_config: Optional header configuration
            footer_config: Optional footer configuration
            logo_bytes: Optional logo image bytes

        Returns:
            Redacted PDF as bytes
        """
        # Find all sensitive data
        sensitive_data = self.find_sensitive_data(redaction_types)

        # Collect all terms to redact
        terms_to_redact = set()

        for data_type, items in sensitive_data.items():
            terms_to_redact.update(items)

        # Perform redaction
        if terms_to_redact:
            self.search_and_redact(terms_to_redact)

        # Add header and footer if provided
        if header_config or footer_config or logo_bytes:
            self.add_header_footer(header_config, footer_config, logo_bytes)

        # Return the redacted PDF as bytes
        return self._export_pdf(output_format)

    def _export_pdf(self, output_format: str) -> bytes:
        """
        Export the PDF in the specified format

        Args:
            output_format: Output format (currently supports 'pdf')

        Returns:
            PDF as bytes
        """
        if output_format.lower() == 'pdf':
            pdf_bytes = self.pdf_document.write()
            return pdf_bytes
        else:
            # Could extend to support other formats (images, etc.)
            raise ValueError(f"Unsupported output format: {output_format}")

    def get_metadata(self) -> Dict:
        """Get PDF metadata"""
        return {
            'page_count': len(self.pdf_document),
            'metadata': self.pdf_document.metadata,
            'is_encrypted': self.pdf_document.is_encrypted
        }

    def close(self):
        """Close the PDF document"""
        self.pdf_document.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class PDFRedactionService:
    """
    High-level service for PDF redaction operations
    """

    SUPPORTED_REDACTION_TYPES = {
        'email': 'Email addresses',
        'phone': 'Phone numbers',
        'linkedin': 'LinkedIn profile URLs',
        'portfolio': 'Portfolio/GitHub URLs',
        'all_urls': 'All URLs'
    }

    SUPPORTED_OUTPUT_FORMATS = ['pdf', 'docx']

    @classmethod
    def validate_redaction_types(cls, redaction_types: List[str]) -> bool:
        """Validate that redaction types are supported"""
        return all(rt in cls.SUPPORTED_REDACTION_TYPES for rt in redaction_types)

    @classmethod
    def validate_output_format(cls, output_format: str) -> bool:
        """Validate output format"""
        return output_format.lower() in cls.SUPPORTED_OUTPUT_FORMATS

    @classmethod
    def get_default_header_footer(cls) -> Dict:
        """Get default Recrui8 header and footer configuration"""
        return {
            'header': DefaultHeaderFooter.get_recrui8_header(),
            'footer': DefaultHeaderFooter.get_recrui8_footer()
        }

    @classmethod
    def process_pdf(cls, pdf_bytes: bytes, redaction_types: List[str],
                   output_format: str = 'pdf', preview_mode: bool = False,
                   header_config: Optional[Dict] = None,
                   footer_config: Optional[Dict] = None,
                   logo_bytes: Optional[bytes] = None,
                   use_default_footer: bool = False) -> Dict:
        """
        Process PDF with redaction

        Args:
            pdf_bytes: PDF file as bytes
            redaction_types: List of data types to redact
            output_format: Output format (default: pdf)
            preview_mode: If True, only return detected data without redacting
            header_config: Optional header configuration
            footer_config: Optional footer configuration
            logo_bytes: Optional logo image bytes
            use_default_footer: Use default Recrui8 footer

        Returns:
            Dictionary with redacted document bytes and metadata
        """
        with PDFProcessor(pdf_bytes) as processor:
            # Get metadata
            metadata = processor.get_metadata()

            # Find sensitive data
            sensitive_data = processor.find_sensitive_data(redaction_types)

            if preview_mode:
                # Preview mode: just return what would be redacted
                return {
                    'preview': True,
                    'sensitive_data': sensitive_data,
                    'metadata': metadata,
                    'redaction_types': redaction_types
                }

            # Use default footer if requested
            if use_default_footer and not footer_config:
                footer_config = DefaultHeaderFooter.get_recrui8_footer()

            # Perform redaction
            redacted_pdf = processor.redact_pdf(
                redaction_types,
                'pdf',  # Always process as PDF first
                header_config,
                footer_config,
                logo_bytes
            )

            # Convert to DOCX if requested
            if output_format.lower() == 'docx':
                redacted_output = DOCXService.process_docx_full(
                    pdf_bytes,
                    redaction_types,
                    header_config,
                    footer_config,
                    logo_bytes
                )
            else:
                redacted_output = redacted_pdf

            return {
                'preview': False,
                'redacted_pdf': redacted_output,
                'sensitive_data_redacted': {k: len(v) for k, v in sensitive_data.items()},
                'metadata': metadata,
                'output_format': output_format
            }
