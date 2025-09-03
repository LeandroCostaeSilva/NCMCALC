import logging
from typing import Dict, List, Tuple

class BrazilianTaxCalculator:
    """
    Calculadora de impostos de importação brasileira
    Implementa as regras tributárias vigentes para importação
    """
    
    # Alíquotas padrão (podem ser sobrescritas por NCM específico)
    DEFAULT_RATES = {
        'II': 0.10,      # Imposto de Importação - 10%
        'IPI': 0.15,     # IPI - 15%
        'PIS': 0.0165,   # PIS-Importação - 1,65%
        'COFINS': 0.076, # COFINS-Importação - 7,6%
        'ICMS': 0.18     # ICMS médio - 18%
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_customs_value(self, unit_value_usd: float, quantity: int, 
                               freight_usd: float = 0, insurance_usd: float = 0, 
                               exchange_rate: float = 5.0) -> Dict[str, float]:
        """
        Calcula o valor aduaneiro (base para cálculo dos impostos)
        """
        fob_value_usd = unit_value_usd * quantity
        cif_value_usd = fob_value_usd + freight_usd + insurance_usd
        cif_value_brl = cif_value_usd * exchange_rate
        
        return {
            'fob_usd': fob_value_usd,
            'cif_usd': cif_value_usd,
            'cif_brl': cif_value_brl,
            'exchange_rate': exchange_rate
        }
    
    def get_tax_rates(self, ncm_code: str) -> Dict[str, float]:
        """
        Obtém as alíquotas específicas para o NCM
        Por enquanto usa alíquotas padrão, mas pode ser integrado com API Siscomex
        """
        # Algumas alíquotas específicas por NCM (exemplos)
        ncm_specific_rates = {
            # Eletrônicos
            '85171200': {'II': 0.16, 'IPI': 0.15, 'PIS': 0.0165, 'COFINS': 0.076, 'ICMS': 0.25},
            '85176200': {'II': 0.20, 'IPI': 0.15, 'PIS': 0.0165, 'COFINS': 0.076, 'ICMS': 0.25},
            # Têxtil
            '62034200': {'II': 0.35, 'IPI': 0.05, 'PIS': 0.0165, 'COFINS': 0.076, 'ICMS': 0.18},
            # Automóveis
            '87032300': {'II': 0.35, 'IPI': 0.25, 'PIS': 0.0165, 'COFINS': 0.076, 'ICMS': 0.12},
        }
        
        return ncm_specific_rates.get(ncm_code, self.DEFAULT_RATES)
    
    def calculate_ii(self, cif_brl: float, rate: float) -> Dict[str, float]:
        """Calcula Imposto de Importação"""
        amount = cif_brl * rate
        return {
            'base_value': cif_brl,
            'rate': rate,
            'amount': amount
        }
    
    def calculate_ipi(self, cif_brl: float, ii_amount: float, rate: float) -> Dict[str, float]:
        """Calcula IPI - base: CIF + II"""
        base_value = cif_brl + ii_amount
        amount = base_value * rate
        return {
            'base_value': base_value,
            'rate': rate,
            'amount': amount
        }
    
    def calculate_pis_cofins(self, cif_brl: float, ii_amount: float, 
                           pis_rate: float, cofins_rate: float) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Calcula PIS e COFINS - base: CIF + II"""
        base_value = cif_brl + ii_amount
        
        pis_amount = base_value * pis_rate
        cofins_amount = base_value * cofins_rate
        
        pis = {
            'base_value': base_value,
            'rate': pis_rate,
            'amount': pis_amount
        }
        
        cofins = {
            'base_value': base_value,
            'rate': cofins_rate,
            'amount': cofins_amount
        }
        
        return pis, cofins
    
    def calculate_icms(self, cif_brl: float, ii_amount: float, ipi_amount: float, 
                      pis_amount: float, cofins_amount: float, rate: float) -> Dict[str, float]:
        """
        Calcula ICMS - base: CIF + II + IPI + PIS + COFINS + próprio ICMS
        Fórmula: ICMS = (Base sem ICMS * alíquota) / (1 - alíquota)
        """
        base_without_icms = cif_brl + ii_amount + ipi_amount + pis_amount + cofins_amount
        icms_amount = (base_without_icms * rate) / (1 - rate)
        base_value = base_without_icms + icms_amount
        
        return {
            'base_value': base_value,
            'rate': rate,
            'amount': icms_amount
        }
    
    def calculate_all_taxes(self, unit_value_usd: float, quantity: int, ncm_code: str,
                           freight_usd: float = 0, insurance_usd: float = 0, 
                           exchange_rate: float = 5.0) -> Dict[str, any]:
        """
        Calcula todos os impostos de importação
        """
        try:
            # 1. Calcular valor aduaneiro
            customs_values = self.calculate_customs_value(
                unit_value_usd, quantity, freight_usd, insurance_usd, exchange_rate
            )
            
            # 2. Obter alíquotas
            rates = self.get_tax_rates(ncm_code)
            
            # 3. Calcular impostos em cascata
            cif_brl = customs_values['cif_brl']
            
            # II
            ii_data = self.calculate_ii(cif_brl, rates['II'])
            
            # IPI
            ipi_data = self.calculate_ipi(cif_brl, ii_data['amount'], rates['IPI'])
            
            # PIS e COFINS
            pis_data, cofins_data = self.calculate_pis_cofins(
                cif_brl, ii_data['amount'], rates['PIS'], rates['COFINS']
            )
            
            # ICMS
            icms_data = self.calculate_icms(
                cif_brl, ii_data['amount'], ipi_data['amount'],
                pis_data['amount'], cofins_data['amount'], rates['ICMS']
            )
            
            # Total dos impostos
            total_taxes = (ii_data['amount'] + ipi_data['amount'] + 
                          pis_data['amount'] + cofins_data['amount'] + icms_data['amount'])
            
            # Custo total
            total_cost = cif_brl + total_taxes
            
            return {
                'customs_values': customs_values,
                'taxes': {
                    'II': ii_data,
                    'IPI': ipi_data,
                    'PIS': pis_data,
                    'COFINS': cofins_data,
                    'ICMS': icms_data
                },
                'summary': {
                    'total_taxes': total_taxes,
                    'total_cost': total_cost,
                    'effective_rate': (total_taxes / cif_brl) * 100
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erro no cálculo de impostos: {str(e)}")
            raise

    def calculate_profitability(self, total_cost_brl: float, selling_price_brl: float,
                               additional_costs: Dict[str, float] = None) -> Dict[str, float]:
        """
        Calcula a rentabilidade da operação
        """
        if additional_costs is None:
            additional_costs = {}
        
        # Custos adicionais
        storage_cost = additional_costs.get('storage', 0)
        marketing_cost = additional_costs.get('marketing', 0)
        platform_fees_rate = additional_costs.get('platform_fees_rate', 0) / 100
        
        # Taxas sobre venda (ICMS, PIS, COFINS sobre venda)
        icms_sale_rate = 0.18  # ICMS sobre venda
        pis_sale_rate = 0.0165
        cofins_sale_rate = 0.076
        
        # Impostos sobre venda
        icms_sale = selling_price_brl * icms_sale_rate
        pis_sale = selling_price_brl * pis_sale_rate
        cofins_sale = selling_price_brl * cofins_sale_rate
        platform_fees = selling_price_brl * platform_fees_rate
        
        total_sale_taxes = icms_sale + pis_sale + cofins_sale + platform_fees
        
        # Custo total final
        total_final_cost = (total_cost_brl + storage_cost + marketing_cost + total_sale_taxes)
        
        # Lucro bruto e líquido
        gross_profit = selling_price_brl - total_cost_brl
        net_profit = selling_price_brl - total_final_cost
        
        # Margens
        gross_margin = (gross_profit / selling_price_brl) * 100 if selling_price_brl > 0 else 0
        net_margin = (net_profit / selling_price_brl) * 100 if selling_price_brl > 0 else 0
        
        # ROI
        roi = (net_profit / total_cost_brl) * 100 if total_cost_brl > 0 else 0
        
        return {
            'selling_price': selling_price_brl,
            'import_cost': total_cost_brl,
            'additional_costs': {
                'storage': storage_cost,
                'marketing': marketing_cost,
                'sale_taxes': total_sale_taxes,
                'platform_fees': platform_fees
            },
            'total_cost': total_final_cost,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
            'gross_margin': gross_margin,
            'net_margin': net_margin,
            'roi': roi
        }
