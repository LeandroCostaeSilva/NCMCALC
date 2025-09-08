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
            'detergente doméstico': ['produto limpeza', 'sabão', 'dish soap'],
            
            # MÁQUINAS E APARELHOS - SEÇÃO XVI
            'máquina': ['aparelho', 'equipamento', 'machine', 'motor', 'gerador'],
            'motor': ['máquina', 'engine', 'motor elétrico', 'propulsão'],
            'gerador': ['máquina', 'generator', 'energia', 'elétrico'],
            'turbina': ['máquina', 'turbine', 'vapor', 'energia'],
            'caldeira': ['máquina', 'vapor', 'boiler', 'aquecimento'],
            'grupo gerador': ['gerador', 'energia', 'eletrogênio', 'motor'],
            'eletrogênio': ['gerador', 'energia', 'grupo gerador'],
            
            # MÓVEIS E DIVERSOS - SEÇÃO XX EXPANDIDO
            'móvel': ['furniture', 'móveis', 'cadeira', 'mesa', 'assento', 'mobiliário', 'mobília'],
            'cadeira': ['assento', 'móvel', 'chair', 'furniture', 'poltrona', 'banco', 'banqueta'],
            'assento': ['cadeira', 'móvel', 'seat', 'furniture', 'poltrona'],
            'mesa': ['table', 'móvel', 'escrivaninha', 'bancada', 'balcão', 'furniture'],
            'sofá': ['sofa', 'móvel', 'canapé', 'divã', 'sofá-cama', 'estofado'],
            'cama': ['bed', 'móvel', 'beliche', 'leito', 'berço', 'furniture'],
            'colchão': ['mattress', 'colchões', 'travesseiro', 'almofada', 'edredom'],
            'armário': ['wardrobe', 'móvel', 'guarda-roupa', 'roupeiro', 'estante'],
            'escritório': ['office', 'corporativo', 'comercial', 'empresarial', 'work'],
            'cozinha': ['kitchen', 'culinário', 'gastronômico', 'cooking'],
            'quarto': ['bedroom', 'dormitório', 'suíte', 'room'],
            'iluminação': ['lighting', 'luminária', 'lustre', 'abajur', 'lâmpada'],
            'brinquedo': ['toy', 'toys', 'jogo', 'boneca', 'criança', 'infantil'],
            'boneca': ['brinquedo', 'doll', 'dolls', 'toy', 'criança', 'boneco'],
            'carrinho': ['brinquedo', 'toy car', 'carrinhos', 'car', 'veículo'],
            'jogo': ['brinquedo', 'game', 'games', 'toy', 'diversão', 'tabuleiro'],
            'videogame': ['console', 'game', 'videogames', 'playstation', 'xbox', 'nintendo'],
            'quebra-cabeça': ['puzzle', 'puzzles', 'jigsaw', 'jogo'],
            'esporte': ['sport', 'sports', 'atlético', 'fitness', 'exercício'],
            'bola': ['ball', 'balls', 'futebol', 'basquete', 'vôlei', 'tênis'],
            'raquete': ['racket', 'raquetes', 'tênis', 'badminton', 'squash'],
            'pesca': ['fishing', 'pescaria', 'anzol', 'vara', 'molinete'],
            'escova': ['brush', 'vassoura', 'limpeza', 'higiene', 'pincel'],
            'vassoura': ['broom', 'escova', 'limpeza', 'varrer'],
            'botão': ['button', 'buttons', 'acessório', 'vestuário', 'fecho'],
            'caneta': ['pen', 'pens', 'esferográfica', 'writing', 'escrita'],
            'lápis': ['pencil', 'pencils', 'grafite', 'lapiseira', 'escrita'],
            'isqueiro': ['lighter', 'isqueiros', 'acendedor', 'fire'],
            'pente': ['comb', 'pentes', 'escova de cabelo', 'hair'],
            'garrafa térmica': ['thermos', 'térmica', 'isotérmica', 'thermal'],
            
            # PRODUTOS QUÍMICOS - SEÇÃO VI
            'químico': ['chemical', 'produto químico', 'substância'],
            'hidrogênio': ['gás', 'chemical', 'elemento químico'],
            'oxigênio': ['gás', 'chemical', 'elemento químico'],
            'nitrogênio': ['gás', 'chemical', 'elemento químico'],
            'cloro': ['chemical', 'elemento químico', 'gás'],
            'carbono': ['chemical', 'elemento químico', 'negro de fumo'],
            'enxofre': ['chemical', 'elemento químico', 'sulfur'],
            'benzeno': ['solvente', 'hidrocarboneto', 'chemical'],
            'tolueno': ['solvente', 'hidrocarboneto', 'chemical'],
            'xileno': ['solvente', 'hidrocarboneto', 'chemical'],
            'estireno': ['monômero', 'hidrocarboneto', 'chemical'],
            'etileno': ['gás', 'hidrocarboneto', 'monômero'],
            'propeno': ['propileno', 'gás', 'hidrocarboneto'],
            'medicamento': ['fármaco', 'remédio', 'droga', 'pharmaceutical'],
            'vacina': ['imunizante', 'biológico', 'medicina'],
            'perfume': ['fragância', 'essência', 'cosmético'],
            'óleo essencial': ['essência', 'aroma', 'perfume'],
            'sabão': ['detergente', 'limpeza', 'higiene'],
            'detergente': ['sabão', 'limpeza', 'tensoativo'],
            'corante': ['tinta', 'pigmento', 'dye', 'colorante'],
            'pigmento': ['corante', 'tinta', 'color', 'colorante'],
            
            # PRODUTOS QUÍMICOS DIVERSOS - CAPÍTULO 38
            'fertilizante': ['adubo', 'ureia', 'nitrato', 'NPK'],
            'adubo': ['fertilizante', 'ureia', 'nitrato', 'NPK'],
            'ureia': ['fertilizante', 'adubo', 'nitrogênio'],
            'pesticida': ['inseticida', 'fungicida', 'herbicida', 'agrotóxico'],
            'inseticida': ['pesticida', 'agrotóxico', 'praguicida'],
            'fungicida': ['pesticida', 'agrotóxico', 'antifúngico'],
            'herbicida': ['pesticida', 'agrotóxico', 'mata-mato'],
            'desinfetante': ['bactericida', 'antisséptico', 'sanitizante'],
            'adesivo': ['cola', 'fixador', 'aderente'],
            'cola': ['adesivo', 'fixador', 'caseína'],
            'gelatina': ['cola animal', 'agar', 'proteína'],
            'enzima': ['catalisador biológico', 'fermento'],
            'catalisador': ['acelerador', 'catalyst', 'reação'],
            'grafita': ['carbono', 'eletrodo', 'grafite'],
            'carvão ativado': ['filtro', 'adsorção', 'purificação'],
            'solvente': ['diluente', 'thinner', 'removedor'],
            'plastificante': ['aditivo plástico', 'flexibilizante'],
            'antioxidante': ['estabilizador', 'conservante'],
            'reagente': ['produto laboratório', 'análise química'],
            
            # PRODUTOS PLÁSTICOS - CAPÍTULO 39
            'plástico': ['polímero', 'resina', 'polietileno', 'PVC'],
            'polímero': ['plástico', 'resina', 'polímeros'],
            'polietileno': ['PE', 'plástico', 'polímero'],
            'polipropileno': ['PP', 'plástico', 'polímero'],
            'PVC': ['policloreto vinila', 'plástico', 'polímero'],
            'poliestireno': ['PS', 'isopor', 'plástico'],
            'ABS': ['acrilonitrila butadieno estireno', 'plástico'],
            'policarbonato': ['PC', 'plástico transparente'],
            'poliamida': ['nylon', 'plástico técnico'],
            'nylon': ['poliamida', 'plástico técnico'],
            'PET': ['politereftalato etileno', 'garrafa plástica'],
            'poliuretano': ['PU', 'espuma', 'elastômero'],
            'silicone': ['silicones', 'elastômero'],
            'resina': ['polímero', 'plástico', 'material sintético'],
            'resina epóxi': ['epoxy', 'adesivo estrutural'],
            'acrílico': ['PMMA', 'metacrilato', 'transparente'],
            'isopor': ['poliestireno expandido', 'EPS'],
            'teflon': ['PTFE', 'politetrafluoroetileno'],
            
            # MÁQUINAS ELETRÔNICAS E COMPUTADORES - CAPÍTULO 84/85
            'máquina eletrônica': ['computador', 'processador', 'digital', 'comunicação bidirecional'],
            'comunicação bidirecional': ['máquina eletrônica', 'digital', 'computador', 'rede'],
            'computador digital': ['máquina eletrônica', 'processador', 'CPU', 'digital'],
            'processamento dados': ['computador', 'máquina eletrônica', 'CPU', 'digital'],
            'unidade processamento': ['CPU', 'processador', 'computador', 'digital'],
            'memória': ['RAM', 'storage', 'armazenamento', 'computador'],
            'entrada saída': ['input', 'output', 'I/O', 'interface', 'computador'],
            
            # ACUMULADORES E PILHAS - CAPÍTULO 8506
            'bateria': ['acumulador', 'pilha', 'battery', 'energia', 'elétrica'],
            'acumulador': ['bateria', 'pilha', 'battery', 'armazenamento energia'],
            'pilha': ['bateria', 'acumulador', 'battery', 'energia'],
            'bateria chumbo': ['acumulador chumbo', 'automotiva', 'arranque'],
            'bateria lítio': ['acumulador lítio', 'lithium', 'ion', 'recarregável'],
            'bateria níquel': ['acumulador níquel', 'NiCad', 'NiMH', 'recarregável'],
            'bateria automotiva': ['acumulador chumbo', 'arranque', 'carro', 'motor'],
            'power bank': ['bateria portátil', 'acumulador', 'carregador portátil'],
            'carregador': ['fonte alimentação', 'adaptador', 'power supply'],
            'fonte alimentação': ['carregador', 'power supply', 'adaptador'],
            
            # PEÇAS AUTOMOTIVAS - CAPÍTULO 8708
            'peça automotiva': ['autopeça', 'auto peça', 'peça carro', 'acessório automotivo'],
            'autopeça': ['peça automotiva', 'auto peça', 'peça carro'],
            'para-choque': ['para-choques', 'parachoque', 'bumper'],
            'freio': ['freios', 'brake', 'pastilha freio', 'disco freio'],
            'amortecedor': ['amortecedores', 'suspensão', 'shock absorber'],
            'radiador': ['sistema refrigeração', 'cooling system', 'arrefecimento'],
            'embreagem': ['clutch', 'disco embreagem', 'platô'],
            'câmbio': ['transmissão', 'caixa velocidades', 'gearbox'],
            'diferencial': ['eixo motor', 'transmissão', 'driveshaft'],
            'volante': ['direção', 'steering wheel', 'caixa direção'],
            'airbag': ['air bag', 'sistema segurança', 'safety'],
            'cinto segurança': ['seat belt', 'sistema segurança', 'safety'],
            'roda': ['rodas', 'wheel', 'aro', 'rim'],
            'pneu': ['pneus', 'tire', 'tyre', 'borracha'],
            'câmara ar': ['inner tube', 'pneu', 'borracha'],
            'escapamento': ['silencioso', 'tubo escape', 'exhaust'],
            'banco': ['assento', 'seat', 'estofamento'],
            'carroçaria': ['body', 'lataria', 'funilaria'],
            'chassi': ['chassis', 'estrutura', 'frame'],
            'tanque combustível': ['reservatório', 'fuel tank', 'combustível'],
            'motor': ['engine', 'propulsor', 'motorização'],
            'bateria automotiva': ['acumulador automotivo', 'bateria carro'],
            
            # CONSTRUÇÃO CIVIL E ALUMÍNIO - CAPÍTULOS 7608, 7610, 7612
            'alumínio': ['aluminum', 'liga alumínio', 'metal alumínio'],
            'construção alumínio': ['estrutura alumínio', 'obra alumínio', 'building'],
            'tubo alumínio': ['tubulação alumínio', 'pipe', 'conduit'],
            'perfil alumínio': ['perfil estrutural', 'extrusão', 'profile'],
            'chapa alumínio': ['folha alumínio', 'placa alumínio', 'sheet'],
            'barra alumínio': ['vergalhão alumínio', 'rod', 'bar'],
            'fio alumínio': ['cabo alumínio', 'wire', 'condutor'],
            'janela alumínio': ['esquadria', 'caixilho', 'window'],
            'porta alumínio': ['folha porta', 'door frame', 'doorway'],
            'grade alumínio': ['tela alumínio', 'mesh', 'screen'],
            'parafuso alumínio': ['porca alumínio', 'rebite', 'fastener'],
            'recipiente alumínio': ['vasilhame', 'container', 'vessel'],
            'tanque alumínio': ['reservatório', 'cisterna', 'tank'],
            'acessório tubo': ['conexão', 'fitting', 'conector'],
            'soleira': ['peitoril', 'threshold', 'sill'],
            'alizares': ['batente', 'trim', 'molding'],
            'caixilho': ['marco', 'frame', 'jamb'],
            'esquadria': ['caixilharia', 'window frame', 'joinery'],
            'estrutura metálica': ['construção metálica', 'steel frame', 'metal building'],
            'obra construção': ['building work', 'construction', 'estrutura'],
            'material construção': ['building material', 'construção civil', 'obra'],
            'tela metálica': ['grade metálica', 'wire mesh', 'screen'],
            'chapa expandida': ['metal expandido', 'expanded metal', 'mesh'],
            'folha metálica': ['sheet metal', 'lâmina', 'foil'],
            
            # VÁLVULAS E EQUIPAMENTOS HIDRÁULICOS - CAPÍTULO 8481
            'válvula': ['valve', 'registro', 'dispositivo controle'],
            'torneira': ['tap', 'faucet', 'spigot', 'válvula'],
            'válvula esfera': ['ball valve', 'válvula bola', 'esférica'],
            'válvula gaveta': ['gate valve', 'válvula guilhotina', 'gaveta'],
            'válvula borboleta': ['butterfly valve', 'válvula disco', 'borboleta'],
            'válvula globo': ['globe valve', 'válvula angular', 'globo'],
            'válvula retenção': ['check valve', 'anti-retorno', 'válvula unidirecional'],
            'válvula segurança': ['safety valve', 'válvula alívio', 'escape'],
            'válvula pressão': ['pressure valve', 'redutora pressão', 'reguladora'],
            'válvula solenóide': ['solenoid valve', 'eletroválvula', 'válvula elétrica'],
            'válvula diafragma': ['diaphragm valve', 'membrana', 'válvula flexível'],
            'válvula pneumática': ['pneumatic valve', 'ar comprimido', 'pneumático'],
            'válvula hidráulica': ['hydraulic valve', 'oleohidráulica', 'hidráulico'],
            'válvula termostática': ['thermostatic valve', 'válvula térmica', 'temperatura'],
            'válvula misturadora': ['mixing valve', 'misturador', 'válvula três vias'],
            'válvula isolamento': ['isolation valve', 'bloqueio', 'fechamento'],
            'válvula controle': ['control valve', 'moduladora', 'automática'],
            'válvula purga': ['bleed valve', 'dreno', 'sangria'],
            'registro pressão': ['pressure gauge', 'manômetro', 'medição'],
            'atuador válvula': ['valve actuator', 'acionador', 'motor válvula'],
            'volante válvula': ['handwheel', 'manivela', 'acionamento manual'],
            'sede válvula': ['valve seat', 'assento', 'vedação'],
            'obturador': ['plug', 'disco válvula', 'elemento vedação'],
            'haste válvula': ['valve stem', 'eixo', 'vara'],
            'castelo válvula': ['valve bonnet', 'tampa', 'cabeçote'],
            'sistema hidráulico': ['hydraulic system', 'oleohidráulico', 'pressão'],
            'sistema pneumático': ['pneumatic system', 'ar comprimido', 'pressão ar'],
            'equipamento hidráulico': ['hydraulic equipment', 'maquinário hidráulico', 'sistema pressão'],
            'controle fluxo': ['flow control', 'regulagem vazão', 'modulação'],
            'redução pressão': ['pressure reduction', 'regulagem pressão', 'controle pressão'],
            
            # JARDINAGEM E FERRAMENTAS - CAPÍTULO 8201
            'ferramenta jardinagem': ['garden tool', 'utensílio jardim', 'equipamento horticultura'],
            'pá jardinagem': ['garden spade', 'shovel', 'escavadeira manual'],
            'enxada': ['hoe', 'sachola', 'cultivador'],
            'ancinho': ['rake', 'rastelo', 'vassoura jardim'],
            'cultivador': ['cultivator', 'escarificador', 'ancinho'],
            'transplantador': ['transplanter', 'plantador', 'ferramenta mudas'],
            'podão': ['pruner', 'tesoura poda', 'alicate poda'],
            'tesoura jardinagem': ['garden scissors', 'pruning shears', 'podadeira'],
            'serra poda': ['pruning saw', 'serrote jardinagem', 'serra galhos'],
            'alicate jardinagem': ['garden pliers', 'alicate poda', 'ferramenta corte'],
            'ferramenta poda': ['pruning tool', 'equipamento poda', 'podadeira'],
            'ferramenta capina': ['weeding tool', 'capinador', 'removedor ervas'],
            'sachola': ['hand hoe', 'enxadinha', 'cultivador pequeno'],
            'ancho': ['mattock', 'picareta jardim', 'ferramenta escavação'],
            'horticultura': ['gardening', 'cultivo plantas', 'jardinagem'],
            'jardinagem': ['gardening', 'horticultura', 'cultivo jardim'],
            
            # PLANTAS E FOLHAGEM - CAPÍTULO 0604
            'folhagem': ['foliage', 'folhas', 'verdura'],
            'folha': ['leaf', 'folhagem', 'verde'],
            'ramo': ['branch', 'galho', 'ramagem'],
            'galho': ['branch', 'ramo', 'vara'],
            'musgo': ['moss', 'briófita', 'vegetação'],
            'líquen': ['lichen', 'organismo', 'crosta'],
            'planta seca': ['dried plant', 'planta desidratada', 'preservada'],
            'planta preservada': ['preserved plant', 'estabilizada', 'tratada'],
            'folhagem tropical': ['tropical foliage', 'folhas tropicais', 'plantas exóticas'],
            'arranjo floral': ['floral arrangement', 'buquê', 'decoração flores'],
            'decoração vegetal': ['plant decoration', 'ornamentação plantas', 'verde decorativo'],
            'ramo decorativo': ['decorative branch', 'galho ornamental', 'vara decoração'],
            'folha tingida': ['dyed leaf', 'folhagem colorida', 'folha tratada'],
            'folha branqueada': ['bleached leaf', 'folhagem clarificada', 'folha processada'],
            'planta estabilizada': ['stabilized plant', 'preservada', 'tratada'],
            'verde preservado': ['preserved greenery', 'folhagem tratada', 'planta conservada'],
            'material vegetal': ['plant material', 'matéria prima vegetal', 'insumo plantas'],
            'produto floricultura': ['floriculture product', 'artigo flores', 'item floral'],
            
            # ENERGIA SOLAR E FOTOVOLTAICA - CAPÍTULOS 8541, 8501
            'placa solar': ['painel solar', 'módulo fotovoltaico', 'solar panel'],
            'painel solar': ['placa solar', 'módulo fotovoltaico', 'painel fotovoltaico'],
            'módulo fotovoltaico': ['painel solar', 'placa solar', 'módulo solar'],
            'célula fotovoltaica': ['célula solar', 'célula PV', 'photovoltaic cell'],
            'célula solar': ['célula fotovoltaica', 'célula PV', 'solar cell'],
            'energia solar': ['fotovoltaica', 'energia fotovoltaica', 'solar energy'],
            'fotovoltaico': ['solar', 'photovoltaic', 'PV'],
            'sistema solar': ['sistema fotovoltaico', 'usina solar', 'geração solar'],
            'sistema fotovoltaico': ['sistema solar', 'instalação solar', 'solar system'],
            'silício monocristalino': ['mono-Si', 'monocrystalline', 'silício mono'],
            'silício policristalino': ['poly-Si', 'polycrystalline', 'silício poli'],
            'silício amorfo': ['a-Si', 'amorphous silicon', 'filme fino'],
            'filme fino': ['thin film', 'silício amorfo', 'tecnologia filme'],
            'módulo bifacial': ['painel bifacial', 'placa dupla face', 'bifacial'],
            'inversor solar': ['inversor fotovoltaico', 'conversor DC-AC', 'solar inverter'],
            'microinversor': ['micro inversor', 'microinverter', 'inversor módulo'],
            'otimizador potência': ['power optimizer', 'otimizador solar', 'MLPE'],
            'controlador carga': ['charge controller', 'regulador carga', 'MPPT'],
            'gerador solar': ['sistema geração solar', 'usina solar', 'solar generator'],
            'cabo solar': ['cabo DC', 'cabo fotovoltaico', 'solar cable'],
            'conector MC4': ['conector solar', 'MC4 connector', 'plug solar'],
            'estrutura fixação': ['suporte painel', 'mounting structure', 'estrutura solar'],
            'string box': ['caixa combinadora', 'DC combiner', 'quadro DC'],
            'fusível solar': ['fuse solar', 'proteção DC', 'fusível fotovoltaico'],
            'disjuntor solar': ['breaker solar', 'proteção AC', 'disjuntor fotovoltaico'],
            'usina solar': ['fazenda solar', 'parque fotovoltaico', 'solar farm'],
            'energia renovável': ['renewable energy', 'energia limpa', 'sustentável'],
            'geração distribuída': ['GD', 'microgeração', 'minigeração'],
            'on grid': ['grid tie', 'conectado rede', 'sistema conectado'],
            'off grid': ['sistema isolado', 'standalone', 'autônomo'],
            'sistema híbrido': ['hybrid system', 'backup solar', 'baterias'],
            'medição bidirecional': ['net metering', 'compensação energia', 'sistema créditos'],

            # TELECOMUNICAÇÕES E CONECTIVIDADE SEM FIO - CAPÍTULO 8517
            'kit alta performance': ['kit performance', 'kit premium', 'equipamento alta performance'],
            'kit mini': ['kit compacto', 'mini kit', 'equipamento compacto'],
            'conexão sem fio': ['wireless', 'wifi', 'sem fio'],
            'roteador wifi': ['router', 'roteador wireless', 'access router'],
            'access point': ['ponto acesso', 'AP', 'wireless access point'],
            'repetidor wifi': ['extensor wifi', 'range extender', 'amplificador wifi'],
            'equipamento mesh': ['rede mesh', 'sistema mesh', 'mesh network'],
            'adaptador usb wifi': ['dongel wifi', 'usb wireless', 'adaptador sem fio'],
            'antena wifi': ['antena wireless', 'antena sem fio', 'wifi antenna'],
            'switch wireless': ['switch wifi', 'comutador sem fio', 'wireless switch'],
            'bridge wifi': ['ponte wifi', 'wireless bridge', 'ponte sem fio'],
            'estação base': ['base station', 'ERB', 'radio base'],
            'repetidor celular': ['amplificador celular', 'booster celular', 'repetidor móvel'],
            'amplificador sinal': ['booster sinal', 'amplificador móvel', 'signal booster'],
            'equipamento satélite': ['comunicação satelital', 'telecomunicação satelital', 'satellite equipment'],
            'antena parabólica': ['dish antenna', 'antena satelital', 'parabolic antenna'],
            'receptor satélite': ['satellite receiver', 'receptor satelital', 'decodificador'],
            'modem satelital': ['satellite modem', 'modem sat', 'terminal satelital'],
            'terminal vsat': ['VSAT terminal', 'very small aperture terminal', 'terminal satelital'],
            'LNB': ['low noise block', 'conversor LNB', 'amplificador baixo ruído'],
            'telefone celular': ['smartphone', 'móvel', 'celular'],
            'telefone sem fio': ['cordless phone', 'telefone wireless', 'sem fio'],
            'videofone': ['video phone', 'telefone vídeo', 'vídeo chamada'],
            'videoconferência': ['video conference', 'conferência vídeo', 'meeting'],
            'modem adsl': ['modem banda larga', 'ADSL modem', 'modem internet'],
            'modem cable': ['cable modem', 'modem cabo', 'modem TV cabo'],
            'modem fibra': ['modem ótico', 'ONT', 'optical network terminal'],
            'gateway': ['roteador gateway', 'porta entrada', 'network gateway'],
            'switch rede': ['comutador', 'network switch', 'switch ethernet'],
            'hub rede': ['concentrador', 'network hub', 'hub ethernet'],
            'conversor mídia': ['media converter', 'conversor rede', 'transceptor'],
            'equipamento voip': ['voice over ip', 'telefonia IP', 'VoIP phone'],
            'antena telecomunicação': ['antenna telecom', 'antena comunicação', 'telecom antenna'],
            'bateria comunicação': ['battery telecom', 'bateria equipamento', 'backup battery'],
            'carregador celular': ['charger phone', 'carregador móvel', 'fonte alimentação'],
            'cabo telecomunicação': ['cabo rede', 'network cable', 'cabo dados'],
            'conector telecomunicação': ['conector rede', 'plug rede', 'network connector'],
            'telecomunicação': ['telecommunication', 'comunicação', 'telecom'],
            'comunicação': ['communication', 'telecomunicação', 'telecom'],
            'conectividade': ['connectivity', 'conexão', 'ligação'],
            'rede sem fio': ['wireless network', 'wifi network', 'rede wifi'],
            'transmissão dados': ['data transmission', 'envio dados', 'comunicação dados'],
            'equipamento rede': ['network equipment', 'dispositivo rede', 'aparelho conectividade'],
            'infraestrutura rede': ['network infrastructure', 'infra rede', 'base comunicação'],
            'sistema comunicação': ['communication system', 'rede comunicação', 'sistema telecom'],

            # CONECTORES ELÉTRICOS E ELETRÔNICOS - POSIÇÃO 8536
            'conector': ['connector', 'plug', 'jack'],
            'conectores cabos planos': ['flat cable connector', 'cabo plano', 'ribbon cable connector'],
            'conector usb': ['USB connector', 'plug USB', 'entrada USB'],
            'conector hdmi': ['HDMI connector', 'plug HDMI', 'entrada HDMI'],
            'conector rj45': ['RJ45 connector', 'ethernet connector', 'plug rede'],
            'conector força': ['power connector', 'plug força', 'tomada elétrica'],
            'conector bnc': ['BNC connector', 'plug BNC', 'conector coaxial'],
            'conector db': ['DB connector', 'D-Sub connector', 'conector serial'],
            'conector circular': ['circular connector', 'conector militar', 'industrial connector'],
            'usb tipo a': ['USB Type A', 'USB-A', 'USB padrão'],
            'usb tipo b': ['USB Type B', 'USB-B', 'USB impressora'],
            'usb tipo c': ['USB Type C', 'USB-C', 'USB reversível'],
            'micro usb': ['Micro USB', 'USB micro', 'conector micro'],
            'mini usb': ['Mini USB', 'USB mini', 'conector mini'],
            'hdmi padrão': ['Standard HDMI', 'HDMI normal', 'HDMI full'],
            'mini hdmi': ['Mini HDMI', 'HDMI mini', 'micro HDMI'],
            'plug rj45': ['RJ45 plug', 'conector ethernet', '8P8C'],
            'jack rj45': ['RJ45 jack', 'entrada ethernet', 'fêmea RJ45'],
            'conector rj11': ['RJ11 connector', 'plug telefone', 'telefone jack'],
            'plug macho': ['male plug', 'conector macho', 'plugue'],
            'tomada elétrica': ['electrical outlet', 'socket', 'entrada energia'],
            'adaptador plug': ['plug adapter', 'conversor plug', 'adaptador tomada'],
            'conector db9': ['DB9 connector', 'serial connector', '9 pin connector'],
            'conector db15': ['DB15 connector', 'VGA connector', '15 pin connector'],
            'conector db25': ['DB25 connector', 'parallel connector', '25 pin connector'],
            'conector vga': ['VGA connector', 'video connector', 'DE15'],
            'conector m12': ['M12 connector', 'circular M12', 'industrial M12'],
            'conector m8': ['M8 connector', 'circular M8', 'sensor connector'],
            'conector militar': ['military connector', 'MIL-DTL', 'spec connector'],
            'conector push pull': ['push-pull connector', 'locking connector', 'twist lock'],
            'conector à prova água': ['waterproof connector', 'IP67 connector', 'sealed connector'],
            'terminal ligação': ['terminal block', 'borne', 'terminal strip'],
            'bloco terminais': ['terminal block', 'terminal strip', 'connection block'],
            'conector banana': ['banana connector', 'banana plug', 'test connector'],
            'conector jacaré': ['alligator clip', 'crocodile clip', 'test clip'],
            'conector bateria': ['battery connector', 'power connector', 'battery terminal'],
            'conector áudio': ['audio connector', 'P2', 'P10'],
            'conector coaxial': ['coaxial connector', 'RF connector', 'antenna connector'],
            'conector fibra óptica': ['fiber optic connector', 'optical connector', 'SC connector'],
            'disjuntor': ['circuit breaker', 'breaker', 'proteção circuito'],
            'disjuntor monopolar': ['single pole breaker', 'monopolar breaker', '1P breaker'],
            'disjuntor bipolar': ['double pole breaker', 'bipolar breaker', '2P breaker'],
            'disjuntor tripolar': ['three pole breaker', 'tripolar breaker', '3P breaker'],
            'disjuntor termomagnético': ['thermal magnetic breaker', 'termo magnético', 'TMB'],
            'disjuntor diferencial': ['GFCI breaker', 'RCD breaker', 'DR'],
            'relé': ['relay', 'contator', 'chave automática'],
            'relé eletromagnético': ['electromagnetic relay', 'EMR', 'mechanical relay'],
            'relé estado sólido': ['solid state relay', 'SSR', 'electronic relay'],
            'relé temporizador': ['timer relay', 'time delay relay', 'temporizador'],
            'relé potência': ['power relay', 'high current relay', 'contactor'],
            'relé industrial': ['industrial relay', 'heavy duty relay', 'control relay'],
            'interruptor': ['switch', 'chave', 'button'],
            'interruptor simples': ['single switch', 'on/off switch', 'toggle switch'],
            'interruptor paralelo': ['three way switch', 'paralelo', 'alternating switch'],
            'comutador rotativo': ['rotary switch', 'selector switch', 'multi position'],
            'chave seccionadora': ['disconnect switch', 'isolator switch', 'seccionador'],
            'micro switch': ['microswitch', 'limit switch', 'snap switch'],
            'soquete lâmpada': ['lamp socket', 'light socket', 'bulb holder'],
            'soquete incandescente': ['incandescent socket', 'E27 socket', 'screw socket'],
            'soquete fluorescente': ['fluorescent socket', 'T8 socket', 'tube socket'],
            'soquete led': ['LED socket', 'lamp holder', 'bulb socket'],
            'porta fusível': ['fuse holder', 'fuse box', 'fusível'],
            'cortacircuito': ['circuit cutter', 'cutout', 'switch'],
            'seccionador': ['disconnector', 'isolator', 'sectionalizer'],
            'dispositivo proteção surto': ['surge protection device', 'SPD', 'DPS'],
            'fusível elétrico': ['electrical fuse', 'fuse', 'proteção sobrecarga'],
            'aparelho proteção': ['protection device', 'safety device', 'circuit protection']
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
