import route53
import argparse
import ipgetter

# Script criado automatizar a criação de Record Sets no Route53 da Amazon AWS de uma zona específica
# Usado para builds dinâmicos de ambientes utilizando o Jenkins
# @author Matheus Scarpato Fidelis
# @email msfidelis01@gmail.com
# @github https://github.com/msfidelis

zone_id = "" # Zone ID do seu domínio
key_id = ""  #Amazon Key ID
access_key = "" #Amazon Access Key
domain = "nanoshots.com.br" # Zone Name


# Retorna o IP atual do servidor -- Usado para fazer o apontamento no Route53 para o servidor
def getserverip():
        return ipgetter.myip()

# Retorna a conexão com a AWS no Route53
def connect():
        return route53.connect(
                aws_access_key_id=key_id,
                aws_secret_access_key=access_key
        )

# Retorna um array no formato que a API da Amazon espera
def construct(zone, subdomain, ip):
        record = "%s.%s" % (subdomain, domain)

        return zone.create_a_record(
                name = record,
                values = [ip]
        )

# Parseia os argumentos e valida se o record set já existe na Amazon
def create():
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--subdomain',help='INFORMA O SUBDOMINIO A SER CRIADO NO RECORD')
        parser.add_argument('-d', '--domain',help='INFORMA O DOMINIO')
        args = parser.parse_args()

        domain = args.domain.strip()
        subdomain = args.subdomain.strip()
        record = "%s.%s" % (subdomain, domain)
        recordaws = "%s." % record

        print getserverip()
        print record
        #sys.exit()

        conn = connect()
        zone = conn.get_hosted_zone_by_id(zone_id)

        #VALIDA SE JA EXISTE UM RECORD NA AMAZON COM O SUBDOMINIO INFORMADO
        for i in zone.record_sets:
                if i.name == recordaws:
                        print "REGISTRO %s JA EXISTENTE NAS ENTRADAS DO ROUTE53 AWS" % record
                        return False


        ip_server = getserverip()
        new_record, change_info = construct(zone, subdomain, ip_server)

        return change_info





print create()
