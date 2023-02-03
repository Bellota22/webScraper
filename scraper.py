import requests
import lxml.html as html #para poder aplicar Xpath
import os #Para crear carpeta con la fecha de hoy
import datetime #traer la fecha de hoy

XPATH_LINK_TO_ARTICLE= '//text-fill/a/@href'
XPATH_TITLE= '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY= '//div[@class="lead"]/p/text()'
XPATH_BODY= '//div[@class="html-content"]/p/text()'

HOME_URL='https://www.larepublica.co/'


def get_title(link):
    #separamos por "/" y nos quedamos con el ultimo que elemento 
    url = link.split('/')[-1]
    #separamos por "-" y eliminamos el ultimo elemento
    title_list=url.split('-')[:-1]
    #Unimos lo anterior
    title = " ".join(title_list)

    return(title)

def parse_notice(link,today):
    try:
        response=requests.get(link) #si el códig es distinto de 200 
        #nos dará un error
        if response.status_code==200:
            notice= response.content.decode('utf-8') #treaemos el html
            parsed= html.fromstring(notice)
            try: #traeremos el titulo, cuerpo y resumen
                title= get_title(link)#trae lista
                title=title.replace('\"','')#Si encontramos comilla doble, eliminada
                summary= parsed.xpath(XPATH_SUMMARY)[0]#trae lista
                body= parsed.xpath(XPATH_BODY)#lista de parrafos, pero yo 
                #quier lista completo
            except IndexError: 
                return #En caso no halla resumen, nos podría dar error, para
                #evitar eso utilizamos la sentencia return

            with open(f'{today}/{title}.txt', 'w',encoding='utf-8') as f:
            #buscaré la carpeta que se creo con la fecha de hoy
            # y dentro de esa carpeta guardare un archivo txt con el titulo
            # de nuestra noticia 
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error:{response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():  #Extrae los links de las noticias
    try:
        response = requests.get(HOME_URL)#Nos devuelve el doc html 
        #y todo lo que involucra http
        if response.status_code==200:
            home=response.content.decode('utf-8')
            #nos devuelve el doc html de la respuesta, decode 
            #transforma los carácteres especiales
            parsed= html.fromstring(home)
            #transforma el contenido de home y lo transforma en un doc
            #especial para poder realizar XPath
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notices)

            today= datetime.date.today().strftime('%d-%m-%Y')
            #Guardamos el formato de la fecha en today
            if not os.path.isdir(today):
                #Si no existe con la carpeta today, la creamos
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link,today)
        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as ve:
        print(ve)

def run(): #Ejecutará el programa
    parse_home()

if __name__== '__main__':
    run()

