"""
Header and Footer Service
Handles adding custom headers and footers to PDF documents
"""
import fitz  # PyMuPDF
from typing import Optional, Dict
import io
import os


class HeaderFooterService:
    """
    Service for adding custom headers and footers to PDFs
    """

    def __init__(self, pdf_document: fitz.Document):
        """
        Initialize with a PDF document

        Args:
            pdf_document: PyMuPDF document object
        """
        self.pdf_document = pdf_document

    def add_header(self, text: Optional[str] = None, logo_bytes: Optional[bytes] = None,
                   logo_position: str = "left", font_size: int = 10):
        """
        Add header to all pages

        Args:
            text: Header text to display
            logo_bytes: Logo image as bytes (PNG, JPG)
            logo_position: Position of logo ("left", "center", "right")
            font_size: Font size for header text
        """
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document[page_num]
            page_width = page.rect.width
            page_height = page.rect.height

            # Header position (top of page)
            header_y = 30

            if logo_bytes:
                # Add logo image
                logo_rect = self._get_logo_rect(page_width, header_y, logo_position)

                # Insert image
                try:
                    page.insert_image(logo_rect, stream=logo_bytes)
                except Exception as e:
                    print(f"Warning: Could not insert logo: {e}")

            if text:
                # Add header text
                text_x = page_width / 2 if not logo_bytes else page_width - 100
                text_rect = fitz.Rect(text_x, header_y - 10, page_width - 20, header_y + 10)

                page.insert_textbox(
                    text_rect,
                    text,
                    fontsize=font_size,
                    align=fitz.TEXT_ALIGN_RIGHT if logo_bytes else fitz.TEXT_ALIGN_CENTER,
                    color=(0, 0, 0)
                )

    def add_footer(self, text: str, font_size: int = 9, align: str = "center"):
        """
        Add footer to all pages

        Args:
            text: Footer text to display
            font_size: Font size for footer text
            align: Text alignment ("left", "center", "right")
        """
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document[page_num]
            page_width = page.rect.width
            page_height = page.rect.height

            # Footer position (bottom of page)
            footer_y = page_height - 30

            # Map alignment
            alignment_map = {
                "left": fitz.TEXT_ALIGN_LEFT,
                "center": fitz.TEXT_ALIGN_CENTER,
                "right": fitz.TEXT_ALIGN_RIGHT
            }

            text_align = alignment_map.get(align, fitz.TEXT_ALIGN_CENTER)

            # Add footer text
            footer_rect = fitz.Rect(20, footer_y - 10, page_width - 20, footer_y + 10)

            page.insert_textbox(
                footer_rect,
                text,
                fontsize=font_size,
                align=text_align,
                color=(0, 0, 0)
            )

    def add_header_footer(self, header_config: Optional[Dict] = None,
                         footer_config: Optional[Dict] = None):
        """
        Add both header and footer based on configuration

        Args:
            header_config: Dictionary with header configuration
                - text: Header text
                - logo_bytes: Logo image bytes
                - logo_position: Logo position
                - font_size: Font size
            footer_config: Dictionary with footer configuration
                - text: Footer text
                - font_size: Font size
                - align: Text alignment
        """
        if header_config:
            self.add_header(
                text=header_config.get('text'),
                logo_bytes=header_config.get('logo_bytes'),
                logo_position=header_config.get('logo_position', 'left'),
                font_size=header_config.get('font_size', 10)
            )

        if footer_config:
            self.add_footer(
                text=footer_config.get('text', ''),
                font_size=footer_config.get('font_size', 9),
                align=footer_config.get('align', 'center')
            )

    def _get_logo_rect(self, page_width: float, y_position: float,
                       position: str = "left") -> fitz.Rect:
        """
        Get rectangle for logo placement

        Args:
            page_width: Width of the page
            y_position: Y position for the logo
            position: Position ("left", "center", "right")

        Returns:
            Rectangle for logo placement
        """
        logo_width = 80
        logo_height = 30

        if position == "left":
            x = 20
        elif position == "center":
            x = (page_width - logo_width) / 2
        else:  # right
            x = page_width - logo_width - 20

        return fitz.Rect(x, y_position - 15, x + logo_width, y_position + 15)


class DefaultHeaderFooter:
    """
    Default header and footer configurations for Recrui8
    """

    @staticmethod
    def get_recrui8_header(include_logo: bool = True) -> Dict:
        """
        Get default Recrui8 header configuration

        Args:
            include_logo: Whether to include logo placeholder

        Returns:
            Header configuration dictionary
        """
        config = {
            'text': None,
            'logo_position': 'left',
            'font_size': 10
        }

        # Note: logo_bytes should be provided separately when available
        return config

    @staticmethod
    def get_recrui8_footer() -> Dict:
        """
        Get default Recrui8 footer configuration

        Returns:
            Footer configuration dictionary
        """
        return {
            'text': 'Recrui8.com | info@Recrui8.com | +91 922-6881-922',
            'font_size': 9,
            'align': 'center'
        }

    @staticmethod
    def get_custom_footer(company_name: str, email: str, phone: str) -> Dict:
        """
        Get custom footer configuration

        Args:
            company_name: Company name/website
            email: Contact email
            phone: Contact phone

        Returns:
            Footer configuration dictionary
        """
        return {
            'text': f'{company_name} | {email} | {phone}',
            'font_size': 9,
            'align': 'center'
        }
