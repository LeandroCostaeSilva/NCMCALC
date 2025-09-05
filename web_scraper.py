import trafilatura
import requests
import logging
from typing import Dict, List
from urllib.parse import urljoin
import time

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    The results is not directly readable, better to be summarized by LLM before consume
    by the user.

    Some common website to crawl information from:
    MLB scores: https://www.mlb.com/scores/YYYY-MM-DD
    """
    # Send a request to the website
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text

class NCMScraper:
    """
    Web scraper para obter dados de códigos NCM do portal oficial
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_expanded_ncm_database(self) -> Dict[str, Dict]:
        """
        Retorna base massivamente expandida de códigos NCM com foco em eletrônicos, químicos, farmacêuticos e domésticos
        """
        return {
            # ELETRÔNICOS E TECNOLOGIA - MASSIVAMENTE EXPANDIDO
            '85171100': {'description': 'Telefones móveis (celulares) e de outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85171200': {'description': 'Telefones para redes celulares ou outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176200': {'description': 'Aparelhos receptores para radiotelefonia ou radiotelegrafia', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176100': {'description': 'Outros aparelhos para recepção, conversão e transmissão ou regeneração de voz, imagens', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '84713000': {'description': 'Máquinas automáticas para processamento de dados, portáteis, de peso não superior a 10 kg', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714100': {'description': 'Outras máquinas automáticas para processamento de dados', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714900': {'description': 'Outras máquinas automáticas para processamento de dados, apresentadas sob a forma de sistemas', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85287200': {'description': 'Aparelhos receptores para televisão, mesmo incorporando um aparelho receptor', 'ii_rate': 0.20, 'ipi_rate': 0.20, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85285200': {'description': 'Monitores e projetores, que não incorporem aparelho receptor de televisão', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85258000': {'description': 'Câmeras de televisão, câmeras fotográficas digitais e câmeras de vídeo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85444200': {'description': 'Cabos coaxiais e outros condutores elétricos coaxiais', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85423100': {'description': 'Processadores e controladores, mesmo combinados com memórias', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85423200': {'description': 'Memórias', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85183000': {'description': 'Fones de ouvido e auscultadores, mesmo combinados com microfone', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85414000': {'description': 'Diodos emissores de luz (LED)', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # PRODUTOS QUÍMICOS - NOVA SEÇÃO EXPANDIDA
            '28011000': {'description': 'Cloro', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28020000': {'description': 'Enxofre sublimado ou precipitado; enxofre coloidal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28061000': {'description': 'Ácido clorídrico (ácido muriático)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28070000': {'description': 'Ácido sulfúrico; óleum', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28080000': {'description': 'Ácido nítrico; ácidos sulfonítricos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041100': {'description': 'Corantes orgânicos sintéticos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32061100': {'description': 'Pigmentos e preparações à base de dióxido de titânio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # PRODUTOS FARMACÊUTICOS - NOVA SEÇÃO EXPANDIDA
            '29411000': {'description': 'Penicilinas e seus derivados, com a estrutura do ácido penicilânico', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29412000': {'description': 'Estreptomicinas e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29413000': {'description': 'Tetraciclinas e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30021000': {'description': 'Antissoros e outras frações do sangue', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30031000': {'description': 'Medicamentos contendo penicilinas ou estreptomicinas', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30033100': {'description': 'Medicamentos contendo insulina', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29362700': {'description': 'Vitamina C e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # UTENSÍLIOS DOMÉSTICOS - MASSIVAMENTE EXPANDIDO
            '73211100': {'description': 'Aparelhos de cozinhar e aquecedores de pratos, de ferro fundido, ferro ou aço', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '73239300': {'description': 'Outros artigos de mesa, cozinha ou outros utensílios domésticos, de aço inoxidável', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '76151100': {'description': 'Artigos de mesa, cozinha ou outros utensílios domésticos, de alumínio', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82111000': {'description': 'Sortidos de facas de mesa de lâmina cortante ou serrilhada', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82159100': {'description': 'Colheres, garfos, conchas, escumadeiras, pás para tortas, facas especiais para peixe ou manteiga', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34011100': {'description': 'Sabões e produtos orgânicos tensoativos para uso na forma de barras, pães, pedaços moldados', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34022000': {'description': 'Preparações tensoativas, preparações para lavagem e preparações para limpeza', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85167100': {'description': 'Aparelhos eletrotérmicos para preparo de café ou chá', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85165000': {'description': 'Fornos de microondas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '70131000': {'description': 'Artigos de vidro dos tipos utilizados para serviço de mesa ou de cozinha', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '69111000': {'description': 'Artigos para serviço de mesa ou de cozinha, de porcelana', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # VESTUÁRIO E MODA
            '61051000': {'description': 'Camisas de malha de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61091000': {'description': 'T-shirts, camisetas interiores e artigos semelhantes de malha de algodão', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61103000': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de malha, de fibras sintéticas ou artificiais', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62034200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62046200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # CALÇADOS
            '64039900': {'description': 'Outros calçados com sola de borracha, plástico, couro natural ou reconstituído', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041900': {'description': 'Outros calçados com sola de borracha ou plástico', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041100': {'description': 'Calçados para esporte; calçados para tênis, basquetebol, ginástica, treinamento e semelhantes', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # COSMÉTICOS E PERFUMARIA
            '33030000': {'description': 'Perfumes e águas-de-colônia', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33041000': {'description': 'Produtos de maquiagem para os lábios', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33049900': {'description': 'Outros produtos de beleza, maquiagem e cuidados da pele', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33051000': {'description': 'Xampus para o cabelo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33061000': {'description': 'Dentifrícios (cremes dentais)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33072000': {'description': 'Desodorantes corporais e antitranspirantes', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # BRINQUEDOS E JOGOS
            '95030010': {'description': 'Triciclos, patinetes, carros de pedal e outros brinquedos semelhantes de rodas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034100': {'description': 'Bonecas que representem exclusivamente seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95036000': {'description': 'Quebra-cabeças (puzzles)', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95041000': {'description': 'Videojogos dos tipos utilizados com receptor de televisão', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # MÓVEIS
            '94035000': {'description': 'Móveis de madeira dos tipos utilizados em dormitórios', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94036000': {'description': 'Outros móveis de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94017100': {'description': 'Assentos com armação de madeira, estofados', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94042900': {'description': 'Colchões de outras matérias', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # ILUMINAÇÃO
            '94051000': {'description': 'Lustres e outros aparelhos elétricos de iluminação, próprios para serem suspensos ou fixados no teto ou na parede', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94052000': {'description': 'Abajures de cabeceira, de escritório e luminárias de interior, elétricos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # ARTIGOS ESPORTIVOS
            '95069100': {'description': 'Artigos e equipamentos para cultura física, ginástica ou atletismo', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95062200': {'description': 'Esquis aquáticos, pranchas de surf e outros equipamentos para esportes aquáticos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95065100': {'description': 'Raquetes de tênis, mesmo não encordoadas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95066100': {'description': 'Bolas de tênis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # JOIAS E RELÓGIOS  
            '71131100': {'description': 'Artigos de joalharia de metais preciosos, de prata', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91011100': {'description': 'Relógios de pulso, elétricos, mesmo com contador de tempo incorporado, com caixa de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # ÓCULOS
            '90041000': {'description': 'Óculos de sol', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90031100': {'description': 'Armações para óculos ou artigos semelhantes, de plástico', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # PRODUTOS ALIMENTÍCIOS
            '18063100': {'description': 'Chocolates e outras preparações alimentícias que contenham cacau, em blocos, tabletes ou barras, recheados', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19053100': {'description': 'Biscoitos doces (bolachas doces)', 'ii_rate': 0.18, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '22021000': {'description': 'Águas, incluindo as águas minerais e as águas gaseificadas, adicionadas de açúcar', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},

            # FERRAMENTAS
            '82013000': {'description': 'Picaretas, pás, cavadeiras, enxadas, sachos, forcados, forquilhas, ancinhos e raspadeiras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82032000': {'description': 'Alicates, tenazes, pinças e ferramentas semelhantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82054000': {'description': 'Chaves de fenda', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # SEÇÃO XVI - MÁQUINAS E APARELHOS, MATERIAL ELÉTRICO (SISCOMEX)
            # Capítulo 84 - Reatores nucleares, caldeiras, máquinas, aparelhos e instrumentos mecânicos
            '84011000': {'description': 'Reatores nucleares', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84012000': {'description': 'Máquinas e aparelhos para a separação isotópica', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84021100': {'description': 'Caldeiras aquatubulares com produção de vapor superior a 45 t por hora', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84021200': {'description': 'Caldeiras aquatubulares com produção de vapor não superior a 45 t por hora', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84022000': {'description': 'Caldeiras denominadas "de água superaquecida"', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84031000': {'description': 'Caldeiras para aquecimento central', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84039000': {'description': 'Outras caldeiras de vapor', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84041000': {'description': 'Aparelhos auxiliares para caldeiras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84042000': {'description': 'Condensadores para máquinas a vapor', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84051000': {'description': 'Geradores de gás de ar (gás pobre) ou de gás de água', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84059000': {'description': 'Outros geradores de gás', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84061000': {'description': 'Turbinas para propulsão de embarcações', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84068100': {'description': 'Turbinas a vapor de potência superior a 40 MW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84068200': {'description': 'Turbinas a vapor de potência não superior a 40 MW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84069000': {'description': 'Partes de turbinas a vapor', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84071000': {'description': 'Motores de aviação', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84072100': {'description': 'Motores fora-de-borda, para embarcações', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84072900': {'description': 'Outros motores marinos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073100': {'description': 'Motores alternativos de cilindrada não superior a 50 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073200': {'description': 'Motores alternativos de cilindrada superior a 50 cm³ mas não superior a 250 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073300': {'description': 'Motores alternativos de cilindrada superior a 250 cm³ mas não superior a 1000 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073400': {'description': 'Motores alternativos de cilindrada superior a 1000 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84081000': {'description': 'Motores de pistão para embarcações', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84082000': {'description': 'Motores de pistão dos tipos utilizados para propulsão de veículos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84089000': {'description': 'Outros motores de pistão', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84091000': {'description': 'Partes para motores de aviação', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84099100': {'description': 'Partes para motores de pistão de ignição por centelha', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84099900': {'description': 'Outras partes para motores de pistão', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 85 - Máquinas, aparelhos e materiais elétricos
            '85011000': {'description': 'Motores de potência não superior a 37,5 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85012000': {'description': 'Motores universais de potência superior a 37,5 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013100': {'description': 'Motores de corrente contínua de potência não superior a 750 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013200': {'description': 'Motores de corrente contínua de potência superior a 750 W mas não superior a 75 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013300': {'description': 'Motores de corrente contínua de potência superior a 75 kW mas não superior a 375 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013400': {'description': 'Motores de corrente contínua de potência superior a 375 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85014000': {'description': 'Motores de corrente alternada, monofásicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85015100': {'description': 'Motores de corrente alternada, polifásicos, de potência não superior a 750 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85015200': {'description': 'Motores de corrente alternada, polifásicos, de potência superior a 750 W mas não superior a 75 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85015300': {'description': 'Motores de corrente alternada, polifásicos, de potência superior a 75 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016100': {'description': 'Geradores de corrente alternada de potência não superior a 75 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016200': {'description': 'Geradores de corrente alternada de potência superior a 75 kVA mas não superior a 375 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016300': {'description': 'Geradores de corrente alternada de potência superior a 375 kVA mas não superior a 750 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016400': {'description': 'Geradores de corrente alternada de potência superior a 750 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85021100': {'description': 'Grupos eletrogênios com motores de pistão de ignição por compressão, de potência não superior a 75 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85021200': {'description': 'Grupos eletrogênios com motores de pistão de ignição por compressão, de potência superior a 75 kVA mas não superior a 375 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85021300': {'description': 'Grupos eletrogênios com motores de pistão de ignição por compressão, de potência superior a 375 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85022000': {'description': 'Grupos eletrogênios com motores de pistão de ignição por centelha', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85023100': {'description': 'Grupos eletrogênios com energia eólica', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85023900': {'description': 'Outros grupos eletrogênios', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # SEÇÃO XX - MERCADORIAS E PRODUTOS DIVERSOS (SISCOMEX)
            # Capítulo 94 - Móveis; mobiliário médico-cirúrgico; colchões, almofadas e semelhantes
            '94011000': {'description': 'Assentos dos tipos utilizados em veículos aéreos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94012000': {'description': 'Assentos dos tipos utilizados em veículos automóveis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94013000': {'description': 'Assentos giratórios, de altura ajustável', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94014000': {'description': 'Assentos transformáveis em camas, exceto o material de acampamento ou de jardim', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94015000': {'description': 'Assentos de vime, vime entrançado, bambu ou matérias semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94016100': {'description': 'Outros assentos, com armação de madeira, estofados', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94016900': {'description': 'Outros assentos, com armação de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94017900': {'description': 'Outros assentos, com armação de metal', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94018000': {'description': 'Outros assentos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94019000': {'description': 'Partes de assentos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 95 - Brinquedos, jogos, artigos para divertimento ou para esporte
            '95011000': {'description': 'Carrinhos para bonecas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95019000': {'description': 'Outros brinquedos de rodas concebidos para serem montados pelas crianças', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95021000': {'description': 'Bonecas que representem exclusivamente seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95029100': {'description': 'Partes e acessórios de bonecas que representem seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95029900': {'description': 'Outras bonecas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95031000': {'description': 'Conjuntos de construção e brinquedos de construção', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95032000': {'description': 'Outros brinquedos de plástico', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95033000': {'description': 'Outros brinquedos de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034000': {'description': 'Outros brinquedos de metal', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95035000': {'description': 'Brinquedos que representem animais ou criaturas não humanas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95037000': {'description': 'Outros brinquedos, conjuntos e sortidos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95038000': {'description': 'Outros brinquedos e modelos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 96 - Obras diversas
            '96031000': {'description': 'Vassouras e escovas de galhos ou de outras matérias vegetais', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96032100': {'description': 'Escovas de dentes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96032900': {'description': 'Outras escovas de barba, para cabelos, para unhas ou para cílios', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96033000': {'description': 'Pincéis e escovas para artistas, pincéis de escrever e pincéis semelhantes para aplicação de produtos cosméticos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96034000': {'description': 'Escovas e pincéis para pintar, caiar, envernizar ou semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96035000': {'description': 'Outras escovas que constituam partes de máquinas, aparelhos ou veículos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96039000': {'description': 'Outras vassouras, escovas, esfregões e espanadores', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96040000': {'description': 'Peneiras e crivos, manuais', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96050000': {'description': 'Sortidos de viagem para toucador de pessoas, para costura ou para limpeza de calçado ou de roupas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96061000': {'description': 'Botões de pressão e suas partes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96062100': {'description': 'Botões de plástico, não recobertos de matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96062200': {'description': 'Botões de metais comuns, não recobertos de matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96062900': {'description': 'Outros botões', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96063000': {'description': 'Formas e outras partes de botões; esboços de botões', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # SEÇÃO VI - PRODUTOS DAS INDÚSTRIAS QUÍMICAS OU DAS INDÚSTRIAS CONEXAS (SISCOMEX)
            # Capítulo 28 - Produtos químicos inorgânicos
            '28011000': {'description': 'Cloro', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28012000': {'description': 'Iodo', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28013000': {'description': 'Flúor; bromo', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28020000': {'description': 'Enxofre sublimado ou precipitado; enxofre coloidal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28030000': {'description': 'Carbono (negros de fumo e outras formas de carbono)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28041000': {'description': 'Hidrogênio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28042100': {'description': 'Argônio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28042900': {'description': 'Outros gases raros', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28043000': {'description': 'Nitrogênio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28044000': {'description': 'Oxigênio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28045000': {'description': 'Boro; telúrio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28046100': {'description': 'Silício com teor de silício superior ou igual a 99,99%, em peso', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28046900': {'description': 'Outro silício', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28047000': {'description': 'Fósforo', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28048000': {'description': 'Arsênio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28049000': {'description': 'Selênio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28051100': {'description': 'Sódio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28051200': {'description': 'Cálcio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28051900': {'description': 'Outros metais alcalinos ou alcalinoterrosos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28053000': {'description': 'Metais de terras raras, escândio e ítrio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28054000': {'description': 'Mercúrio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 29 - Produtos químicos orgânicos  
            '29011000': {'description': 'Hidrocarbonetos acíclicos saturados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29012100': {'description': 'Etileno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29012200': {'description': 'Propeno (propileno)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29012300': {'description': 'Buteno (butileno) e seus isômeros', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29012400': {'description': 'Buta-1,3-dieno e isopreno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29012900': {'description': 'Outros hidrocarbonetos acíclicos não saturados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29021100': {'description': 'Ciclopentano, cicloexano e cicloeptano', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29021900': {'description': 'Outros hidrocarbonetos cicloparafínicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29022000': {'description': 'Benzeno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29023000': {'description': 'Tolueno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29024100': {'description': 'o-Xileno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29024200': {'description': 'm-Xileno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29024300': {'description': 'p-Xileno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29024400': {'description': 'Isômeros do xileno em mistura', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29025000': {'description': 'Estireno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29026000': {'description': 'Etilbenzeno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29027000': {'description': 'Cumeno', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29029000': {'description': 'Outros hidrocarbonetos aromáticos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 30 - Produtos farmacêuticos
            '30011000': {'description': 'Glândulas e outros órgãos para usos opoterápicos, dessecados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30012000': {'description': 'Extratos de glândulas ou de outros órgãos ou das suas secreções', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30013000': {'description': 'Heparina e seus sais', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30019000': {'description': 'Outras substâncias humanas ou animais preparadas para usos terapêuticos', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30021000': {'description': 'Antissoros e outras frações do sangue', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30022000': {'description': 'Vacinas para medicina humana', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30023000': {'description': 'Vacinas para medicina veterinária', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30024000': {'description': 'Toxinas e culturas de microrganismos', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30029000': {'description': 'Outros sangues humano e animal preparados para usos terapêuticos', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 32 - Extratos tanantes e tintoriais; taninos e seus derivados; pigmentos e outras matérias corantes
            '32011000': {'description': 'Extratos de acácia (cassate)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32012000': {'description': 'Extratos de mimosa', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32019000': {'description': 'Outros extratos tanantes de origem vegetal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32020000': {'description': 'Taninos e seus sais, éteres, ésteres e outros derivados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32030000': {'description': 'Matérias corantes de origem vegetal ou animal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041100': {'description': 'Corantes dispersos e preparações à base destes corantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041200': {'description': 'Corantes ácidos e preparações à base destes corantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041300': {'description': 'Corantes básicos e preparações à base destes corantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041400': {'description': 'Corantes diretos e preparações à base destes corantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041500': {'description': 'Corantes à tina (incluindo os utilizáveis diretamente como corantes pigmentários)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041600': {'description': 'Corantes reativos e preparações à base destes corantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041700': {'description': 'Corantes pigmentários e preparações à base destes corantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041900': {'description': 'Outros corantes orgânicos sintéticos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 33 - Óleos essenciais e resinóides; produtos de perfumaria ou de toucador
            '33011100': {'description': 'Óleos essenciais de bergamota', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33011200': {'description': 'Óleos essenciais de laranja', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33011300': {'description': 'Óleos essenciais de limão', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33011900': {'description': 'Outros óleos essenciais de frutos cítricos', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012100': {'description': 'Óleos essenciais de gerânio', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012200': {'description': 'Óleos essenciais de jasmim', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012300': {'description': 'Óleos essenciais de lavanda (alfazema) ou de lavandin', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012400': {'description': 'Óleos essenciais de hortelã-pimenta (Mentha piperita)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012500': {'description': 'Óleos essenciais de outras mentas', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012600': {'description': 'Óleos essenciais de vetiver', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33012900': {'description': 'Outros óleos essenciais', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 34 - Sabões, agentes orgânicos de superfície, preparações para lavagem
            '34011100': {'description': 'Sabões e produtos orgânicos tensoativos para uso na forma de barras', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34011900': {'description': 'Outros sabões, produtos orgânicos tensoativos', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34012000': {'description': 'Sabões sob outras formas', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34013000': {'description': 'Produtos orgânicos tensoativos para lavagem da pele', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34021100': {'description': 'Agentes orgânicos de superfície aniônicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34021200': {'description': 'Agentes orgânicos de superfície catiônicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34021300': {'description': 'Agentes orgânicos de superfície não iônicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34021900': {'description': 'Outros agentes orgânicos de superfície', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34022000': {'description': 'Preparações tensoativas, preparações para lavagem e preparações para limpeza', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 31 - Adubos (fertilizantes)
            '31010000': {'description': 'Adubos de origem animal ou vegetal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31021000': {'description': 'Ureia, mesmo em solução aquosa', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31022100': {'description': 'Sulfato de amônio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31022900': {'description': 'Outros sais duplos e misturas de nitrato de cálcio e sulfato de amônio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31023000': {'description': 'Nitrato de amônio, mesmo em solução aquosa', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31024000': {'description': 'Misturas de nitrato de amônio com carbonato de cálcio ou outras matérias inorgânicas sem poder fertilizante', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31025000': {'description': 'Nitrato de sódio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31026000': {'description': 'Sais duplos e misturas de nitrato de cálcio e nitrato de amônio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31027000': {'description': 'Cianamida cálcica', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31028000': {'description': 'Misturas de ureia e nitrato de amônio em solução aquosa ou amoniacal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '31029000': {'description': 'Outros adubos minerais ou químicos nitrogenados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 35 - Matérias albuminoides; produtos à base de amidos ou de féculas modificados; colas; enzimas
            '35011000': {'description': 'Caseínas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35012000': {'description': 'Caseinatos e outros derivados das caseínas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35013000': {'description': 'Colas de caseína', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35021100': {'description': 'Albuminas de ovo, dessecadas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35021900': {'description': 'Outras albuminas de ovo', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35022000': {'description': 'Albuminas do leite (lactoalbuminas)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35029000': {'description': 'Outras albuminas, albuminatos e outros derivados das albuminas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35030000': {'description': 'Gelatinas e seus derivados; ictiocola; outras colas de origem animal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35040000': {'description': 'Peptonas e seus derivados; outras matérias proteicas e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35051000': {'description': 'Dextrinas e outros amidos e féculas modificados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35052000': {'description': 'Colas à base de amidos ou de féculas, de dextrinas ou de outros amidos ou féculas modificados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35061000': {'description': 'Produtos próprios para serem utilizados como colas ou adesivos, acondicionados para venda a retalho como colas ou adesivos, com peso líquido não superior a 1 kg', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35069100': {'description': 'Adesivos à base de polímeros das posições 39.01 a 39.13 ou de borracha', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35069900': {'description': 'Outras colas e outros adesivos preparados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35071000': {'description': 'Coalho e seus concentrados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '35079000': {'description': 'Outras enzimas; enzimas preparadas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 38 - PRODUTOS DIVERSOS DAS INDÚSTRIAS QUÍMICAS (AMPLIAÇÃO MASSIVA)
            '38011000': {'description': 'Grafita artificial', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38012000': {'description': 'Grafita coloidal ou semicoloidal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38013000': {'description': 'Pastas carbonáceas para eletrodos e pastas semelhantes para revestimento interior de fornos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38019000': {'description': 'Outras preparações à base de grafita ou de outros carbonos, em pastas, blocos, plaquetas ou outras semimanufaturas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38021000': {'description': 'Carvões ativados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38029000': {'description': 'Outras matérias minerais ativadas; negro de origem animal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38030000': {'description': 'Tall oil, mesmo refinado', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38040000': {'description': 'Lixívias residuais da fabricação das pastas de celulose', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38051000': {'description': 'Essências de terebintina, de pinheiro ou provenientes da fabricação da pasta de papel ao sulfato', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38052000': {'description': 'Óleo de pinho', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38059000': {'description': 'Outros óleos essenciais brutos de coníferas; terpenos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38061000': {'description': 'Colofônias e ácidos resínicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38062000': {'description': 'Sais de colofônias, de ácidos resínicos ou de derivados de colofônias ou de ácidos resínicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38063000': {'description': 'Gomas éster', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38069000': {'description': 'Outros derivados de colofônias e de ácidos resínicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38070000': {'description': 'Alcatrão de madeira; óleo de alcatrão de madeira; creosoto de madeira; naftaleno metílico; breu vegetal; breu de cervejaria e preparações semelhantes à base de colofônias, de ácidos resínicos ou de breu vegetal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38081000': {'description': 'Inseticidas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38082000': {'description': 'Fungicidas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38083000': {'description': 'Herbicidas, inibidores de germinação e reguladores do crescimento de plantas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38084000': {'description': 'Desinfetantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38085000': {'description': 'Outros pesticidas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38089100': {'description': 'Inseticidas à base de piretróides', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38089200': {'description': 'Fungicidas à base de compostos de cobre', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38089300': {'description': 'Herbicidas à base de ésteres do ácido 2,4-diclorofenoxiacético', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38089900': {'description': 'Outros pesticidas não especificados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38091000': {'description': 'Produtos para acabamento de couros e peles com base de amidos ou de fécula', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38099100': {'description': 'Produtos para acabamento de matérias têxteis', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38099200': {'description': 'Produtos para acabamento de papel e cartão', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38099300': {'description': 'Produtos para acabamento de couro e peles', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38101000': {'description': 'Preparações para decapagem de metais; fluxos para soldar e outras preparações auxiliares para soldagem de metais', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38109000': {'description': 'Outras preparações para decapagem; pastas e pós para soldar', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38111000': {'description': 'Preparações antidetonantes à base de compostos de chumbo', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38112100': {'description': 'Aditivos para óleos lubrificantes contendo óleos de petróleo ou de minerais betuminosos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38112900': {'description': 'Outros aditivos para óleos lubrificantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38119000': {'description': 'Outras preparações antidetonantes, inibidores de oxidação, aditivos peptizantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38121000': {'description': 'Aceleradores de vulcanização preparados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38122000': {'description': 'Plastificantes compostos para borracha ou matérias plásticas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38123000': {'description': 'Preparações antioxidantes e outros estabilizadores compostos para borracha ou matérias plásticas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38130000': {'description': 'Composições extintoras; granadas e bombas extintoras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38140000': {'description': 'Solventes e diluentes orgânicos compostos; preparações concebidas para remover tintas ou vernizes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38151100': {'description': 'Catalisadores suportados tendo como substância ativa o níquel ou um composto de níquel', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38151200': {'description': 'Catalisadores suportados tendo como substância ativa um metal precioso ou um composto de metal precioso', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38151900': {'description': 'Outros catalisadores suportados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38159000': {'description': 'Outras preparações catalisadoras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38160000': {'description': 'Cimentos, argamassas, concretos e composições semelhantes, refratários', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38170000': {'description': 'Misturas de alquilbenzenos e misturas de alquilnaftalenos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38180000': {'description': 'Elementos químicos dopados para uso em eletrônica, em discos, plaquetas ou formas análogas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38190000': {'description': 'Fluidos para freios hidráulicos e outros fluidos preparados para transmissões hidráulicas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38200000': {'description': 'Preparações anticongelantes e fluidos descongelantes preparados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38210000': {'description': 'Meios de cultura preparados para o desenvolvimento e a manutenção de microrganismos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38220000': {'description': 'Reagentes de diagnóstico ou de laboratório sobre qualquer suporte', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38231100': {'description': 'Ácido esteárico', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38231200': {'description': 'Ácido oleico', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38231300': {'description': 'Ácidos gordos do tall oil', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38231900': {'description': 'Outros ácidos gordos monocarboxílicos industriais; óleos ácidos de refinação', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38237000': {'description': 'Álcoois gordos industriais', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38241000': {'description': 'Aglutinantes preparados para moldes ou para núcleos de fundição', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38249100': {'description': 'Misturas e preparações contendo haletos de metais das terras raras, de ítrio ou de escândio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '38249900': {'description': 'Outros produtos químicos e preparações das indústrias químicas ou das indústrias conexas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18}
        }

# Instância global do serviço
ncm_scraper = NCMScraper()