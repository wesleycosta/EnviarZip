# coding=utf-8
import smtplib
import zipfile
from email import encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from threading import Thread

# CONFIGURAÇÃO DO SERVIDOR DE SMTP
remetente = "seu e-mail"
senha = "sua senha"
servidorSmtp = "smtp.gmail.com"
portaSmtp = 587
corpo = "I'M BATMAN"


def enviarEmail(assunto, destinatario, nomeArquivo):
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    body = corpo

    msg.attach(MIMEText(body, 'plain'))

    filename = nomeArquivo
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    try:
        server = smtplib.SMTP(servidorSmtp, portaSmtp)
        server.starttls()
        server.login(remetente, senha)
        text = msg.as_string()
        server.sendmail(remetente, destinatario, text)
        server.quit()
        return True
    except:
        return False


def extrairArquivo(arquivo, senha, nomeArquivo, destinatario):
    try:
        arquivo.extractall(pwd=senha)
        print('[+] Senha encontrada: ' + senha + '\n')

        assunto = "Senha do arquivo zip e " + senha
        enviado = enviarEmail(assunto, destinatario, nomeArquivo)

        if enviado == True:
            print '[+] E-mail enviado com sucesso para: ' + destinatario
        else:
            print '[-] Falha ao enviar o e-mail'
    except:
        pass


def inicio():
    nomeArquivo = "mal.zip"
    arquivoZipe = zipfile.ZipFile(nomeArquivo)
    arquivoDici = open("dicionario.txt")
    destinatario = "seu email de destino"

    for linha in arquivoDici.readlines():
        senha = linha.strip('\n')
        t = Thread(target=extrairArquivo, args=(arquivoZipe, senha, nomeArquivo, destinatario))
        t.start()


if __name__ == '__main__':
    inicio()
