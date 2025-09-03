import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

class CurrencyService:
    """
    Serviço para obter cotações de moeda
    Integra com APIs do Banco Central e AwesomeAPI
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        self.cache_duration = timedelta(minutes=30)  # Cache por 30 minutos
    
    def get_usd_brl_rate(self) -> float:
        """
        Obtém a cotação USD/BRL atual
        """
        cache_key = 'USD_BRL'
        current_time = datetime.now()
        
        # Verificar cache
        if (cache_key in self.cache and 
            current_time - self.cache[cache_key]['timestamp'] < self.cache_duration):
            return self.cache[cache_key]['rate']
        
        try:
            # Tentar AwesomeAPI primeiro
            rate = self._get_rate_from_awesome_api()
            if rate:
                self.cache[cache_key] = {
                    'rate': rate,
                    'timestamp': current_time
                }
                return rate
        except Exception as e:
            self.logger.warning(f"Erro ao obter cotação da AwesomeAPI: {str(e)}")
        
        try:
            # Fallback para Banco Central
            rate = self._get_rate_from_bcb()
            if rate:
                self.cache[cache_key] = {
                    'rate': rate,
                    'timestamp': current_time
                }
                return rate
        except Exception as e:
            self.logger.warning(f"Erro ao obter cotação do BCB: {str(e)}")
        
        # Fallback para cotação padrão
        self.logger.warning("Usando cotação padrão de R$ 5,00")
        return 5.0
    
    def _get_rate_from_awesome_api(self) -> Optional[float]:
        """
        Obtém cotação da AwesomeAPI
        """
        try:
            url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rate = float(data['USDBRL']['bid'])
            
            self.logger.info(f"Cotação obtida da AwesomeAPI: R$ {rate:.4f}")
            return rate
            
        except Exception as e:
            self.logger.error(f"Erro na AwesomeAPI: {str(e)}")
            return None
    
    def _get_rate_from_bcb(self) -> Optional[float]:
        """
        Obtém cotação do Banco Central do Brasil
        """
        try:
            # API do BCB para cotação do dólar
            today = datetime.now().strftime('%m-%d-%Y')
            url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda='USD'&@dataCotacao='{today}'&$format=json"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data['value']:
                rate = float(data['value'][0]['cotacaoVenda'])
                self.logger.info(f"Cotação obtida do BCB: R$ {rate:.4f}")
                return rate
            
        except Exception as e:
            self.logger.error(f"Erro na API do BCB: {str(e)}")
            return None
    
    def get_historical_rates(self, days: int = 30) -> Dict[str, float]:
        """
        Obtém histórico de cotações (para gráficos)
        """
        try:
            url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{days}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            historical_rates = {}
            
            for item in data:
                date = datetime.fromtimestamp(int(item['timestamp'])).strftime('%Y-%m-%d')
                rate = float(item['bid'])
                historical_rates[date] = rate
            
            return historical_rates
            
        except Exception as e:
            self.logger.error(f"Erro ao obter histórico de cotações: {str(e)}")
            return {}
    
    def format_currency_brl(self, amount: float) -> str:
        """
        Formata valor em BRL
        """
        return f"R$ {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def format_currency_usd(self, amount: float) -> str:
        """
        Formata valor em USD
        """
        return f"US$ {amount:,.2f}"
