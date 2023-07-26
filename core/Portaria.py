from reportlab.lib.pagesizes import letter
from core.Documento import Documento


class Portaria(Documento):

    font_name = "Helvetica"
    linha_comprimento = 550
    LOGO_VERTICAL = letter[1] - 100
    LINHA_VERTICAL = LOGO_VERTICAL - (-20)

    def draw_header(self, pdf):

        logo_path = '/Users/gabrielcarlos/Desktop/Codigos/uea-news/templates/static/images/logo-governo.jpg'
        logo_width = 270
        logo_height = 115
        logo_x = (letter[0] - logo_width) / 2
        LINHA_VERTICAL = self.LOGO_VERTICAL - (-20)

        pdf.drawImage(logo_path, logo_x, self.LOGO_VERTICAL, logo_width, logo_height)
        pdf.line(self._centralizar_X(self.linha_comprimento), self.LINHA_VERTICAL, (letter[0] + self.linha_comprimento) / 2, LINHA_VERTICAL)

    def draw_footer(self, pdf):

        font_size = 10
        LINHA_VERTICAL = self.LOGO_VERTICAL - (-20)
        FOOTER_TEXT = "Governo do Estado do Amazonas"
        FOOTER_TEXT_VERTICAL = (letter[0] - pdf.stringWidth(FOOTER_TEXT, self.font_name, font_size)) / 2
        FOOTER_TEXT_HORIZONTAL = 32
        
        FOOTER_TEXT_2 = "Av. Brasil, 3925 - Compensa II - Manaus-AM - CEP 69036-110"
        FOOTER_TEXT2_VERTICAL = (letter[0] - pdf.stringWidth(FOOTER_TEXT_2, self.font_name, font_size)) / 2
        FOOTER_TEXT2_HORIZONTAL = FOOTER_TEXT_HORIZONTAL - font_size - 8

        pdf.line(self._centralizar_X(self.linha_comprimento), self.LINHA_VERTICAL - 655, (letter[0] + self.linha_comprimento) / 2, LINHA_VERTICAL - 655)

        pdf.setFont(self.font_name, font_size)
        pdf.drawString(FOOTER_TEXT_VERTICAL, FOOTER_TEXT_HORIZONTAL, FOOTER_TEXT)

        pdf.setFont(self.font_name, font_size)
        pdf.drawString(FOOTER_TEXT2_VERTICAL, FOOTER_TEXT2_HORIZONTAL, FOOTER_TEXT_2)
