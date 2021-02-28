import pathlib
from json import dumps
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import FirefoxProfile, Options
from scraper.converte_inteiro import converte_inteiro


FF_PROF_DIR = '/home/woitek/.mozilla/firefox/4sqh9j98.Selenium'
FF_EXE_PATH = str(pathlib.Path(__file__).parent / 'geckodriver')


def pega_firefox_profile(profile_directory):
    p = pathlib.Path(profile_directory)

    if p.exists() and p.is_dir():
        return FirefoxProfile(profile_directory=profile_directory)
    return None


class Imovel():
    def __init__(self, elemento):
        self.elemento = elemento

        self.endereco = self.pega_endereco()
        self.area = self.pega_area()
        self.quartos = self.pega_quartos()
        self.banheiros = self.pega_banheiros()
        self.vagas = self.pega_vagas()
        self.preco = self.pega_preco()

        del self.elemento


    def __str__(self):
        return dumps(
            {
                'endereco': self.endereco,
                'area': self.area,
                'quartos': self.quartos,
                'banheiros': self.banheiros,
                'vagas': self.vagas,
                'preco': self.preco,
            }
        )


    def pega_item(self, classe, tag=None, inicio=0):
        try:
            item = self.elemento.find_element_by_class_name(classe)
        except NoSuchElementException:
            return ''

        if tag is not None:
            try:
                item = item.find_element_by_tag_name(tag)
            except NoSuchElementException:
                return ''

        item = item.text.strip()[inicio:]
        return item


    def pega_endereco(self):
        return self.pega_item(classe='property-card__address')


    def pega_area(self):
        area = self.pega_item(
            classe=(
                'property-card__detail-value'
                '.js-property-card-value'
                '.property-card__detail-area'
                '.js-property-card-detail-area'
            )
        )
        return converte_inteiro(area)


    def pega_quartos(self):
        quartos = self.pega_item(
            classe=(
                'property-card__detail-item'
                '.property-card__detail-room'
                '.js-property-detail-rooms'
            ),
            tag='span'
        )
        return converte_inteiro(quartos)


    def pega_banheiros(self):
        banheiros = self.pega_item(
            classe=(
                'property-card__detail-item'
                '.property-card__detail-bathroom'
                '.js-property-detail-bathroom'
            ),
            tag='span'
        )
        return converte_inteiro(banheiros)


    def pega_vagas(self):
        vagas = self.pega_item(
            classe=(
                'property-card__detail-item'
                '.property-card__detail-garage'
                '.js-property-detail-garages'
            ),
            tag='span'
        )
        vagas = vagas.replace('--', '0')
        return converte_inteiro(vagas)


    def pega_preco(self):
        preco = self.pega_item(
            classe=(
                'property-card__price'
                '.js-property-card-prices'
                '.js-property-card__price-small'
            ),
            tag='p',
            inicio=3
        )
        preco = preco.replace('.', '')
        return converte_inteiro(preco)


class ImoveisScraper(webdriver.Firefox):
    def __init__(
        self,
        url,
        pags=1,
        saida='saida.jl',
        espera=10,
        headless=False
    ):
        ff_opts = Options()
        ff_opts.headless = headless

        super().__init__(
            firefox_profile=pega_firefox_profile(FF_PROF_DIR),
            executable_path=FF_EXE_PATH,
            firefox_options=ff_opts
        )
        self.implicitly_wait(15)

        self.url = url
        self.pags = pags
        self.saida = saida
        self.espera = espera


    def pega_imoveis(self):
        return (
            self
            .find_element_by_class_name('results__main')
            .find_elements_by_class_name('property-card__content')
        )


    def vai_para_proxima(self):
        proxima = self.find_element_by_partial_link_text('Próxima')
        clicou = False

        while not clicou:
            try:
                proxima.click()
                clicou = True
            except ElementClickInterceptedException:
                self.execute_script('window.scrollBy(0, 50)')

        sleep(self.espera)


    def raspa_cidade(self, verbose=False):
        self.get(self.url)

        with open(self.saida, 'a') as arquivo:
            for _ in range(self.pags):
                for i in self.pega_imoveis():
                    imovel_str = str(Imovel(i))
                    arquivo.write(imovel_str + '\n')

                    if verbose:
                        print(imovel_str)

                self.vai_para_proxima()
