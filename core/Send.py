import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def Email(email, nome_laboratorio, responsavel):
    try:
        servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_email.starttls()

        servidor_email.login('gcgabriel257@gmail.com', 'kkenkrbtbzidpznv')

        remetente = 'gcgabriel257@gmail.com'
        assunto = 'Assunto: Criação de Novo Laboratório na UEA'
        destinatarios = email
        mensagem = MIMEMultipart()

        with open('uea-news/templates/static/images/logo_email.png', 'rb') as img_file:
            imagem = MIMEImage(img_file.read())
            imagem.add_header('Content-ID', '<logo>')
            mensagem.attach(imagem)
                    
        conteudo = """
            <p>Prezado {responsavel},</p>
            <p>
            Gostaria de informar que foi criado um novo laboratório no sistema CampusLab da Universidade do Estado do Amazonas (UEA), denominado "Laboratório {nome}" e você foi denominado como responsável. 

            Se você deseja colaborar, visualizar ou editar projetos dentro do Laboratório {nome}, entre no link informado: <a href= "http://0.0.0.0:8001/autenticacao/deslogar/"> Aberte aqui para ir ao Laboratorio  </a>
            </p>

            <p>Atenciosamente,</p>
            <p><b>Universidade do Estado do Amazonas (UEA)</b></p>
            
            <img src='cid:logo' alt="Logotipo UEA"
            style="width: 250px; height: 100px;"/>
        """.format(nome=nome_laboratorio, responsavel=responsavel)

        mensagem['From'] = remetente
        mensagem['To'] = destinatarios
        mensagem['Subject'] = assunto

        conteudo = MIMEText(conteudo, 'html', 'utf-8')
        mensagem.attach(conteudo)
        
        servidor_email.sendmail(remetente, destinatarios, mensagem.as_string())

    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    finally:
        servidor_email.quit()

    