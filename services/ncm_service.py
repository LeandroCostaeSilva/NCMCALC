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
        Carrega base de dados NCM expandida com milhares de códigos organizados por categoria
        """
        # Importar base expandida do scraper
        from web_scraper import ncm_scraper
        expanded_db = ncm_scraper.get_expanded_ncm_database()
        
        # Retornar base expandida diretamente
        return expanded_db
    
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
        
        # Mapeamento massivamente expandido de termos comuns para NCM
        term_mapping = {
            # ELETRÔNICOS E TECNOLOGIA
            'celular': ['telefone', 'smartphone', 'móvel', 'cellular', 'phone', 'iphone', 'android', 'galaxy', 'xiaomi'],
            'smartphone': ['telefone', 'celular', 'móvel', 'phone', 'iphone', 'android', 'galaxy', 'samsung'],
            'telefone': ['celular', 'smartphone', 'móvel', 'phone'],
            'computador': ['máquina processamento', 'notebook', 'laptop', 'pc', 'desktop', 'cpu', 'processamento dados'],
            'notebook': ['computador', 'laptop', 'portátil', 'ultrabook', 'macbook'],
            'laptop': ['notebook', 'computador', 'portátil', 'ultrabook'],
            'tablet': ['ipad', 'computador', 'portátil', 'eletrônico'],
            'tv': ['televisão', 'televisor', 'aparelho receptor', 'smart tv'],
            'televisão': ['tv', 'televisor', 'aparelho receptor', 'smart tv'],
            'câmera': ['camera', 'fotográfica', 'digital', 'vídeo', 'filmadora'],
            'fone': ['headphone', 'earphone', 'ouvido', 'áudio'],
            'headphone': ['fone', 'ouvido', 'áudio'],
            
            # VESTUÁRIO E MODA
            'camiseta': ['t-shirt', 'camisa', 'blusa', 'malha', 'algodão'],
            'camisa': ['camiseta', 't-shirt', 'blusa', 'social'],
            'calça': ['pants', 'jeans', 'bermuda', 'short', 'jardineira'],
            'jeans': ['calça', 'denim', 'pants'],
            'vestido': ['dress', 'feminino', 'roupa mulher'],
            'saia': ['skirt', 'feminino', 'roupa mulher'],
            'blusa': ['camisa', 'camiseta', 'feminino', 'roupa mulher'],
            'suéter': ['pullover', 'cardigan', 'colete', 'malha'],
            'casaco': ['paletó', 'jaqueta', 'agasalho', 'sobretudo'],
            'maiô': ['biquíni', 'swimsuit', 'banho'],
            'biquíni': ['maiô', 'swimsuit', 'banho'],
            'sutiã': ['soutien', 'lingerie', 'íntimo feminino'],
            'calcinha': ['lingerie', 'íntimo feminino'],
            'cueca': ['íntimo masculino', 'underwear'],
            
            # CALÇADOS
            'tênis': ['calçado', 'sapato', 'esportivo', 'sneaker', 'running', 'esporte'],
            'sapato': ['calçado', 'shoe', 'social', 'couro'],
            'sandália': ['calçado', 'sandal', 'chinelo'],
            'bota': ['boot', 'calçado', 'couro'],
            'chinelo': ['sandália', 'flip-flop', 'calçado'],
            
            # BOLSAS E ACESSÓRIOS
            'bolsa': ['mala', 'bagagem', 'artigo couro', 'bag', 'handbag', 'feminino'],
            'mala': ['bolsa', 'bagagem', 'viagem', 'suitcase', 'travel'],
            'carteira': ['wallet', 'couro', 'acessório'],
            'cinto': ['belt', 'couro', 'acessório'],
            'relógio': ['watch', 'tempo', 'cronômetro', 'pulso'],
            'óculos': ['glasses', 'solar', 'vista', 'armação', 'ray-ban'],
            'joias': ['joia', 'jewelry', 'ouro', 'prata', 'bijuteria'],
            'bijuteria': ['joia', 'jewelry', 'acessório'],
            
            # CASA E MÓVEIS
            'móvel': ['mobiliário', 'casa', 'madeira', 'furniture'],
            'mesa': ['table', 'móvel', 'madeira'],
            'cadeira': ['chair', 'assento', 'móvel'],
            'sofá': ['sofa', 'móvel', 'estofado'],
            'cama': ['bed', 'móvel', 'dormitório'],
            'guarda-roupa': ['armário', 'móvel', 'dormitório'],
            'luminária': ['lâmpada', 'iluminação', 'abajur'],
            'espelho': ['mirror', 'vidro', 'casa'],
            'panela': ['utensílio', 'cozinha', 'cooking'],
            'prato': ['utensílio', 'cozinha', 'louça'],
            
            # BRINQUEDOS E JOGOS
            'brinquedo': ['toy', 'jogos', 'diversão', 'criança', 'infantil'],
            'boneca': ['doll', 'brinquedo', 'criança'],
            'carrinho': ['toy car', 'brinquedo', 'criança'],
            'lego': ['blocos', 'construção', 'brinquedo'],
            'quebra-cabeça': ['puzzle', 'jogo', 'brinquedo'],
            'videogame': ['console', 'game', 'eletrônico', 'playstation', 'xbox'],
            
            # COSMÉTICOS E PERFUMARIA
            'cosmético': ['beleza', 'maquiagem', 'cuidado', 'beauty'],
            'perfume': ['fragrância', 'cosmético', 'colônia'],
            'batom': ['lipstick', 'maquiagem', 'lábios'],
            'base': ['foundation', 'maquiagem', 'rosto'],
            'shampoo': ['xampu', 'cabelo', 'higiene'],
            'condicionador': ['cabelo', 'higiene'],
            'creme': ['loção', 'hidratante', 'pele'],
            'protetor solar': ['sunscreen', 'proteção', 'pele'],
            'desodorante': ['antitranspirante', 'higiene'],
            'sabonete': ['soap', 'higiene', 'banho'],
            
            # ESPORTES
            'bola': ['ball', 'futebol', 'basquete', 'vôlei'],
            'raquete': ['racket', 'tênis', 'badminton'],
            'equipamento esportivo': ['sport', 'exercício', 'ginástica'],
            'patins': ['skate', 'rodas', 'esporte'],
            'bicicleta': ['bike', 'ciclismo', 'esporte'],
            'prancha': ['surf', 'esporte aquático'],
            
            # ALIMENTOS E BEBIDAS
            'alimento': ['comida', 'alimentício', 'preparação', 'food'],
            'bebida': ['líquido', 'água', 'refrigerante', 'drink'],
            'chocolate': ['doce', 'cacau', 'sweet'],
            'biscoito': ['cookie', 'bolacha', 'doce'],
            'água': ['water', 'bebida', 'mineral'],
            'suco': ['juice', 'bebida', 'fruta'],
            
            # FERRAMENTAS
            'ferramenta': ['tool', 'equipamento', 'utensílio', 'trabalho'],
            'chave': ['wrench', 'ferramenta', 'fenda'],
            'martelo': ['hammer', 'ferramenta'],
            'alicate': ['plier', 'ferramenta'],
            
            # AUTOMÓVEIS
            'automóvel': ['carro', 'veículo', 'motor', 'car'],
            'carro': ['automóvel', 'veículo', 'car'],
            'moto': ['motocicleta', 'motorcycle', 'veículo'],
            'peça': ['part', 'acessório', 'componente'],
            
            # QUÍMICOS E PRODUTOS QUÍMICOS - EXPANDIDO
            'químico': ['produto químico', 'chemical', 'reagente', 'ácido', 'solvente', 'corante', 'pigmento', 'tinta', 'detergente'],
            'ácido': ['químico', 'reagente', 'acid', 'chemical', 'corrosivo', 'industrial'],
            'solvente': ['químico', 'thinner', 'diluente', 'chemical', 'industrial'],
            'tinta': ['pigmento', 'corante', 'paint', 'químico', 'verniz', 'esmalte'],
            'detergente': ['produto limpeza', 'químico', 'soap', 'sabão', 'limpeza'],
            'corante': ['pigmento', 'tinta', 'dye', 'químico'],
            'pigmento': ['corante', 'tinta', 'químico', 'colorante'],
            'cloro': ['químico', 'desinfetante', 'chlorine'],
            'enxofre': ['químico', 'sulfur', 'industrial'],
            
            # FARMACÊUTICOS E MEDICAMENTOS - EXPANDIDO
            'remédio': ['medicamento', 'medicine', 'drug', 'farmacêutico', 'comprimido', 'cápsula', 'pílula'],
            'medicamento': ['remédio', 'medicine', 'drug', 'farmacêutico', 'pharmaceutical'],
            'antibiótico': ['medicamento', 'penicilina', 'medicine', 'antibiotic'],
            'penicilina': ['antibiótico', 'medicamento', 'penicillin'],
            'vitamina': ['suplemento', 'medicamento', 'vitamin', 'nutritional'],
            'suplemento': ['vitamina', 'medicamento', 'supplement', 'nutricional'],
            'insulina': ['medicamento', 'diabético', 'hormone', 'insulin'],
            'vacina': ['imunização', 'medicamento', 'vaccine', 'immunization'],
            'soro': ['medicamento', 'serum', 'antissoro'],
            'comprimido': ['medicamento', 'pílula', 'tablet', 'pill'],
            'cápsula': ['medicamento', 'remédio', 'capsule'],
            
            # UTENSÍLIOS DOMÉSTICOS ESPECÍFICOS - EXPANDIDO
            'panela': ['utensílio', 'cozinha', 'cooking', 'pan', 'pot'],
            'frigideira': ['panela', 'utensílio', 'cozinha', 'frying pan'],
            'prato': ['utensílio', 'cozinha', 'louça', 'dish', 'plate'],
            'copo': ['utensílio', 'vidro', 'bebida', 'glass', 'cup'],
            'garfo': ['talher', 'utensílio', 'fork', 'cutlery'],
            'faca': ['talher', 'utensílio', 'knife', 'cutlery'],
            'colher': ['talher', 'utensílio', 'spoon', 'cutlery'],
            'talher': ['garfo', 'faca', 'colher', 'cutlery', 'utensílio'],
            'microondas': ['eletrodoméstico', 'microwave', 'forno'],
            'cafeteira': ['eletrodoméstico', 'coffee maker', 'café'],
            'torradeira': ['eletrodoméstico', 'toaster', 'pão'],
            'ferro': ['eletrodoméstico', 'iron', 'passar roupa'],
            'aspirador': ['eletrodoméstico', 'vacuum', 'limpeza'],
            'detergente doméstico': ['produto limpeza', 'sabão', 'dish soap']
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
