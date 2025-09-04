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
            '82054000': {'description': 'Chaves de fenda', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18}
        }

# Instância global do serviço
ncm_scraper = NCMScraper()