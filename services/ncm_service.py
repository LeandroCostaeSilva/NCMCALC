import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app import db
from models import NcmCache

class NCMService:
    """
    Serviço para busca e cache de informações de códigos NCM
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Base de dados NCM expandida com códigos organizados por categoria
        self.ncm_database = self._load_ncm_database()
    
    def _load_ncm_database(self) -> Dict[str, Dict]:
        """
        Carrega base de dados NCM com códigos organizados por categoria
        """
        return {
            # ELETRÔNICOS E TECNOLOGIA
            '85171200': {'description': 'Telefones para redes celulares ou outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176200': {'description': 'Aparelhos receptores para radiotelefonia ou radiotelegrafia', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85171100': {'description': 'Telefones móveis celulares e smartphones', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85444200': {'description': 'Cabos coaxiais e outros condutores elétricos coaxiais', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85234900': {'description': 'Outros discos, fitas e outros suportes para gravação de som ou gravações análogas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85287200': {'description': 'Aparelhos receptores para televisão, mesmo incorporando um aparelho receptor de radiodifusão ou um aparelho de gravação ou reprodução de som ou imagens', 'ii_rate': 0.20, 'ipi_rate': 0.20, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84713000': {'description': 'Máquinas automáticas para processamento de dados, portáteis', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714100': {'description': 'Máquinas automáticas para processamento de dados que contenham, numa mesma unidade, pelo menos uma unidade central de processamento, uma unidade de entrada e uma unidade de saída', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85258000': {'description': 'Câmeras de televisão, câmeras fotográficas digitais e câmeras de vídeo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # VESTUÁRIO E MODA
            '62034200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61103000': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de fibras sintéticas ou artificiais', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62052000': {'description': 'Camisas de fibras sintéticas ou artificiais, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62046200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61051000': {'description': 'Camisas de malha de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61091000': {'description': 'T-shirts, camisetas interiores e artigos semelhantes de malha de algodão', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62033100': {'description': 'Paletós (casacos) de lã ou pelos finos, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62114200': {'description': 'Macacões (fatos-macacos) e conjuntos de esqui, de fibras sintéticas ou artificiais para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61124000': {'description': 'Maiôs e biquínis de malha de fibras sintéticas ou artificiais', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62121000': {'description': 'Soutiens (sutiãs) de qualquer matéria têxtil', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # CALÇADOS E ACESSÓRIOS
            '64039900': {'description': 'Outros calçados com sola de borracha, plástico, couro natural ou reconstituído', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041900': {'description': 'Outros calçados com sola de borracha ou plástico', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64032000': {'description': 'Outros calçados com sola de couro natural e parte superior que cubra o tornozelo', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64051000': {'description': 'Outros calçados com parte superior de couro natural', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90041000': {'description': 'Óculos de sol', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90031900': {'description': 'Outras armações de óculos e armações semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71131900': {'description': 'Outros artigos de joalharia de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71171900': {'description': 'Bijuterias de outros metais comuns', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # ARTIGOS DE COURO E BAGAGEM
            '42021200': {'description': 'Malas, maletas e artigos semelhantes, com superfície exterior de plástico ou matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42021100': {'description': 'Malas, maletas e artigos semelhantes, com superfície exterior de couro natural, couro reconstituído ou couro envernizado', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42022100': {'description': 'Bolsas, mesmo com alça, normalmente carregadas na mão, com superfície exterior de couro natural, couro reconstituído ou couro envernizado', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42022200': {'description': 'Bolsas, mesmo com alça, normalmente carregadas na mão, com superfície exterior de folhas de plástico ou matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42023100': {'description': 'Artigos de bolso ou de bolsa de mão, com superfície exterior de couro natural, couro reconstituído ou couro envernizado', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42031000': {'description': 'Vestuário de couro natural ou couro reconstituído', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # AUTOMÓVEIS E VEÍCULOS
            '87032300': {'description': 'Automóveis com motor alternativo de ignição por centelha, cilindrada > 1500 cm3 mas <= 3000 cm3', 'ii_rate': 0.35, 'ipi_rate': 0.25, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '87032100': {'description': 'Automóveis com motor alternativo de ignição por centelha, cilindrada <= 1000 cm3', 'ii_rate': 0.35, 'ipi_rate': 0.25, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '87032200': {'description': 'Automóveis com motor alternativo de ignição por centelha, cilindrada > 1000 cm3 mas <= 1500 cm3', 'ii_rate': 0.35, 'ipi_rate': 0.25, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '87033100': {'description': 'Automóveis com motor diesel ou semi-diesel, cilindrada <= 1500 cm3', 'ii_rate': 0.35, 'ipi_rate': 0.25, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '87089900': {'description': 'Outras partes e acessórios de carrocerias para veículos automóveis', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '87141000': {'description': 'Partes e acessórios de motocicletas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # CASA E JARDIM
            '73211100': {'description': 'Aparelhos de cozinhar e aquecedores de pratos, de ferro fundido, ferro ou aço', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '73239300': {'description': 'Outros artigos de mesa, cozinha ou outros utensílios domésticos, de aço inoxidável', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94036000': {'description': 'Outros móveis de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94035000': {'description': 'Móveis de madeira dos tipos utilizados em dormitórios', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94054000': {'description': 'Outros aparelhos de iluminação elétrica', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94017900': {'description': 'Outros assentos com armação de metal', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '68022900': {'description': 'Outras pedras de cantaria ou de construção trabalhadas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '63049200': {'description': 'Outros artigos de cama, de fibras sintéticas ou artificiais', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # BRINQUEDOS E JOGOS
            '95030000': {'description': 'Brinquedos de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95032000': {'description': 'Brinquedos com motor elétrico', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034900': {'description': 'Outros jogos de construção', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95051000': {'description': 'Artigos para festas de Natal', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95089000': {'description': 'Outros carrosséis, balanços, barracas de tiro ao alvo e outras diversões de parque', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # COSMÉTICOS E CUIDADOS PESSOAIS
            '33049900': {'description': 'Outros produtos de beleza, maquiagem e cuidados da pele', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33051000': {'description': 'Xampus', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33053000': {'description': 'Lacas para o cabelo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33059000': {'description': 'Outras preparações capilares', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33061000': {'description': 'Dentifrícios', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33079000': {'description': 'Outras preparações para barbear, desodorantes corporais e antitranspirantes', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34011100': {'description': 'Sabões e produtos orgânicos tensoativos para uso na forma de barras, pães, pedaços moldados ou formas semelhantes', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # FERRAMENTAS E EQUIPAMENTOS
            '82013000': {'description': 'Picaretas, pás, cavadeiras, enxadas, sachos, forcados, forquilhas, ancinhos e raspadeiras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82032000': {'description': 'Alicates, tenazes, pinças e ferramentas semelhantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82054000': {'description': 'Chaves de fenda', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82055100': {'description': 'Outras ferramentas de mão dos tipos utilizados na agricultura, horticultura ou silvicultura', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84669200': {'description': 'Partes e acessórios para máquinas-ferramentas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # ARTIGOS ESPORTIVOS
            '95069100': {'description': 'Artigos e equipamentos para ginástica, atletismo, outros esportes ou jogos ao ar livre', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95062900': {'description': 'Outras bolas infláveis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95065100': {'description': 'Raquetes de tênis, mesmo não encordoadas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95067000': {'description': 'Patins de gelo e patins de rodas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # PRODUTOS ALIMENTÍCIOS
            '21069000': {'description': 'Outras preparações alimentícias', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '18063200': {'description': 'Outros chocolates e outras preparações alimentícias que contenham cacau, em blocos, tabletes ou barras, com peso superior a 2 kg', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19053200': {'description': 'Bolachas doces (biscoitos doces) e waffles e wafers', 'ii_rate': 0.18, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '20019000': {'description': 'Outras preparações de produtos hortícolas, fruta ou de outras partes de plantas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '22021000': {'description': 'Águas, incluindo as águas minerais e as águas gaseificadas', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12}
        }
    
    def search_ncm(self, query: str) -> List[Dict[str, str]]:
        """
        Busca códigos NCM por código ou descrição com busca inteligente
        """
        query = query.lower().strip()
        results = []
        exact_matches = []
        partial_matches = []
        
        # Palavras-chave para diferentes categorias de produtos
        search_terms = self._expand_search_query(query)
        
        for code, data in self.ncm_database.items():
            description_lower = data['description'].lower()
            
            # Busca exata por código
            if query in code:
                exact_matches.append({
                    'code': code,
                    'description': data['description'],
                    'score': 100
                })
                continue
            
            # Busca por termos expandidos
            score = 0
            for term in search_terms:
                if term in description_lower:
                    score += 20
                elif any(word in description_lower for word in term.split()):
                    score += 10
            
            # Busca original
            if query in description_lower:
                score += 30
            elif any(word in description_lower for word in query.split()):
                score += 15
            
            if score > 0:
                partial_matches.append({
                    'code': code,
                    'description': data['description'],
                    'score': score
                })
        
        # Ordenar por score
        partial_matches.sort(key=lambda x: x['score'], reverse=True)
        
        # Combinar resultados
        all_results = exact_matches + partial_matches
        
        # Remover score do resultado final
        for result in all_results:
            result.pop('score', None)
        
        # Limitar resultados
        return all_results[:15]
    
    def _expand_search_query(self, query: str) -> List[str]:
        """
        Expande a busca com sinônimos e termos relacionados
        """
        query = query.lower()
        expansions = [query]
        
        # Mapeamento de termos comuns para NCM
        term_mapping = {
            'celular': ['telefone', 'smartphone', 'móvel'],
            'smartphone': ['telefone', 'celular', 'móvel'],
            'camiseta': ['t-shirt', 'camisa', 'blusa'],
            'tênis': ['calçado', 'sapato', 'esportivo'],
            'sapato': ['calçado', 'tênis'],
            'bolsa': ['mala', 'bagagem', 'artigo couro'],
            'mala': ['bolsa', 'bagagem', 'viagem'],
            'computador': ['máquina processamento', 'notebook', 'laptop'],
            'notebook': ['computador', 'laptop', 'portátil'],
            'brinquedo': ['jogos', 'diversão', 'criança'],
            'cosmético': ['beleza', 'maquiagem', 'cuidado'],
            'perfume': ['fragrância', 'cosmético'],
            'relógio': ['tempo', 'cronômetro'],
            'óculos': ['solar', 'vista', 'armação'],
            'automóvel': ['carro', 'veículo', 'motor'],
            'carro': ['automóvel', 'veículo'],
            'móvel': ['mobiliário', 'casa', 'madeira'],
            'ferramenta': ['equipamento', 'utensílio'],
            'roupa': ['vestuário', 'têxtil', 'confecção'],
            'alimento': ['comida', 'alimentício', 'preparação'],
            'bebida': ['líquido', 'água', 'refrigerante']
        }
        
        # Adicionar expansões baseadas no mapeamento
        for term, synonyms in term_mapping.items():
            if term in query:
                expansions.extend(synonyms)
        
        # Remover duplicatas
        return list(set(expansions))
    
    def get_ncm_info(self, ncm_code: str) -> Optional[Dict]:
        """
        Obtém informações completas de um código NCM
        """
        ncm_code = ncm_code.replace('.', '').replace('-', '').strip()
        
        # Verificar cache no banco
        cached = self._get_from_cache(ncm_code)
        if cached and cached.expires_at > datetime.utcnow():
            return {
                'code': cached.code,
                'description': cached.description,
                'rates': {
                    'ii_rate': cached.ii_rate,
                    'ipi_rate': cached.ipi_rate,
                    'pis_rate': cached.pis_rate,
                    'cofins_rate': cached.cofins_rate,
                    'icms_rate': cached.icms_rate
                }
            }
        
        # Buscar na base local
        if ncm_code in self.ncm_database:
            data = self.ncm_database[ncm_code]
            
            # Salvar no cache
            self._save_to_cache(ncm_code, data)
            
            return {
                'code': ncm_code,
                'description': data['description'],
                'rates': {
                    'ii_rate': data['ii_rate'],
                    'ipi_rate': data['ipi_rate'],
                    'pis_rate': data['pis_rate'],
                    'cofins_rate': data['cofins_rate'],
                    'icms_rate': data['icms_rate']
                }
            }
        
        return None
    
    def _get_from_cache(self, ncm_code: str) -> Optional[NcmCache]:
        """
        Obtém NCM do cache
        """
        try:
            return NcmCache.query.filter_by(code=ncm_code).first()
        except Exception as e:
            self.logger.error(f"Erro ao buscar NCM no cache: {str(e)}")
            return None
    
    def _save_to_cache(self, ncm_code: str, data: Dict):
        """
        Salva NCM no cache
        """
        try:
            # Remover entrada existente
            existing = NcmCache.query.filter_by(code=ncm_code).first()
            if existing:
                db.session.delete(existing)
            
            # Criar nova entrada
            cache_entry = NcmCache()
            cache_entry.code = ncm_code
            cache_entry.description = data['description']
            cache_entry.ii_rate = data['ii_rate']
            cache_entry.ipi_rate = data['ipi_rate']
            cache_entry.pis_rate = data['pis_rate']
            cache_entry.cofins_rate = data['cofins_rate']
            cache_entry.icms_rate = data['icms_rate']
            cache_entry.expires_at = datetime.utcnow() + timedelta(days=30)
            
            db.session.add(cache_entry)
            db.session.commit()
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar NCM no cache: {str(e)}")
            db.session.rollback()
    
    def get_popular_ncms(self) -> List[Dict[str, str]]:
        """
        Retorna lista de NCMs mais utilizados
        """
        popular_codes = ['85171200', '85176200', '62034200', '64039900', '61103000']
        results = []
        
        for code in popular_codes:
            if code in self.ncm_database:
                results.append({
                    'code': code,
                    'description': self.ncm_database[code]['description']
                })
        
        return results
    
    def validate_ncm_code(self, ncm_code: str) -> bool:
        """
        Valida formato do código NCM
        """
        ncm_code = ncm_code.replace('.', '').replace('-', '').strip()
        return len(ncm_code) == 8 and ncm_code.isdigit()
