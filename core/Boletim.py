from core.Documento import Documento
from reportlab.lib import colors

class Boletim (Documento):

    logo_width = 650
    logo_height = 850
    FONT = 'Helvetica-Bold'
    FOTN_SIZE = 25
    HEADER_LOGO_PATH = '/home/lury/Área de Trabalho/projeto/uea-news/templates/static/images/boletim (1).jpg'
    
    def desenharCapa(self, pdf, capaImage, portaria):
        
        pdf.drawImage(capaImage, 0, 0, width=self.logo_width, height=self.logo_height)

        pdf.setFillColor(colors.white)

        pdf.setFont(self.FONT, self.FOTN_SIZE)

        TITULO_LARGURA = pdf.stringWidth(portaria, self.FONT, self.FOTN_SIZE)

        pdf.drawString(
            self._centralizar_X(TITULO_LARGURA), 
            self._centralizar_Y(TITULO_LARGURA), 
            portaria
        )

        pdf.showPage()

    def draw_header(self, pdf):
        pdf.drawImage(self.HEADER_LOGO_PATH, 0, 0, width=self.logo_width, height=self.logo_height)

    def desenharNumeracaoDocumento(self, pdf, textWidth, text):

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(self._centralizar_X(textWidth), 750, text)

    def desenharSubtituloNumeracaoDocumento(self, pdf, textWidth, text):

        pdf.setFont('Helvetica', 12)
        pdf.drawString(self._centralizar_X(textWidth), 730, text)

    def desenharContraCapa(self, pdf, titulo, subtitulo):

        self.draw_header(pdf)

        TITLE_WIDTH = pdf.stringWidth(titulo, 'Helvetica-Bold', 12)
        self.desenharNumeracaoDocumento(pdf, TITLE_WIDTH, titulo)

        SUBTITLE_WIDTH = pdf.stringWidth(subtitulo, 'Helvetica-Bold', 12)
        self.desenharSubtituloNumeracaoDocumento(pdf, SUBTITLE_WIDTH, subtitulo)

        # pdf.drawString(self._centralizar_X(autoridade1Largura), 580, autoridade1)
        # pdf.drawString(self._centralizar_X(autoridade2Largura), 480, autoridade2)

    def desenharSumario(self, pdf, titulo, subtitulo):

        self.draw_header(pdf)

        TITLE_WIDTH = pdf.stringWidth(titulo, 'Helvetica-Bold', 12)
        self.desenharNumeracaoDocumento(pdf, TITLE_WIDTH, titulo)

        SUBTITLE_WIDTH = pdf.stringWidth(subtitulo, 'Helvetica-Bold', 12)
        self.desenharSubtituloNumeracaoDocumento(pdf, SUBTITLE_WIDTH, subtitulo)
        