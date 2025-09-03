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
        
        # Base de dados NCM simplificada para o MVP
        self.ncm_database = {
            '85171200': {
                'description': 'Telefones para redes celulares ou outras redes sem fio',
                'ii_rate': 0.16,
                'ipi_rate': 0.15,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.25
            },
            '85176200': {
                'description': 'Aparelhos receptores para radiotelefonia ou radiotelegrafia',
                'ii_rate': 0.20,
                'ipi_rate': 0.15,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.25
            },
            '62034200': {
                'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para homens ou rapazes',
                'ii_rate': 0.35,
                'ipi_rate': 0.05,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            },
            '87032300': {
                'description': 'Automóveis com motor alternativo de ignição por centelha, cilindrada > 1500 cm3 mas <= 3000 cm3',
                'ii_rate': 0.35,
                'ipi_rate': 0.25,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.12
            },
            '64039900': {
                'description': 'Outros calçados com sola de borracha, plástico, couro natural ou reconstituído',
                'ii_rate': 0.35,
                'ipi_rate': 0.15,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            },
            '61103000': {
                'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de fibras sintéticas ou artificiais',
                'ii_rate': 0.35,
                'ipi_rate': 0.05,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            },
            '42021200': {
                'description': 'Malas, maletas e artigos semelhantes, com superfície exterior de plástico ou matérias têxteis',
                'ii_rate': 0.20,
                'ipi_rate': 0.15,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            },
            '73211100': {
                'description': 'Aparelhos de cozinhar e aquecedores de pratos, de ferro fundido, ferro ou aço',
                'ii_rate': 0.20,
                'ipi_rate': 0.10,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            },
            '95030000': {
                'description': 'Brinquedos de madeira',
                'ii_rate': 0.20,
                'ipi_rate': 0.30,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            },
            '90041000': {
                'description': 'Óculos de sol',
                'ii_rate': 0.20,
                'ipi_rate': 0.15,
                'pis_rate': 0.0165,
                'cofins_rate': 0.076,
                'icms_rate': 0.18
            }
        }
    
    def search_ncm(self, query: str) -> List[Dict[str, str]]:
        """
        Busca códigos NCM por código ou descrição
        """
        query = query.lower().strip()
        results = []
        
        for code, data in self.ncm_database.items():
            if (query in code or 
                query in data['description'].lower()):
                results.append({
                    'code': code,
                    'description': data['description']
                })
        
        # Limitar resultados
        return results[:10]
    
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
            cache_entry = NcmCache(
                code=ncm_code,
                description=data['description'],
                ii_rate=data['ii_rate'],
                ipi_rate=data['ipi_rate'],
                pis_rate=data['pis_rate'],
                cofins_rate=data['cofins_rate'],
                icms_rate=data['icms_rate'],
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            
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
