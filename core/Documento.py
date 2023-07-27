from reportlab.lib.pagesizes import letter

class Documento: 

    def _centralizar_X(self, text):
        return ((letter[0] - text) / 2)
    
    def _centralizar_Y(self, text):
        return (letter[1] / 2)
    
    