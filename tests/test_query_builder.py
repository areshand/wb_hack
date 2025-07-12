import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from query_builder import QueryBuilder

class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = QueryBuilder()
    
    def test_extract_address(self):
        prompt = "What's the balance of 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
        address = self.builder.extract_address(prompt)
        self.assertEqual(address, "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b")
    
    def test_extract_address_39_chars(self):
        prompt = "What's the current balance of 0x3Cc19ad349C4afC532673CfA4a561517Aa7cfB84?"
        address = self.builder.extract_address(prompt)
        self.assertEqual(address, "0x3Cc19ad349C4afC532673CfA4a561517Aa7cfB84")
    
    def test_extract_address_none(self):
        prompt = "What's the balance of my wallet?"
        address = self.builder.extract_address(prompt)
        self.assertIsNone(address)
    
    def test_extract_token_symbol(self):
        prompt = "What's the volume of PEPE token?"
        symbol = self.builder.extract_token_symbol(prompt)
        self.assertEqual(symbol, "PEPE")
    
    def test_extract_token_symbol_case_insensitive(self):
        prompt = "What's the volume of pepe token?"
        symbol = self.builder.extract_token_symbol(prompt)
        self.assertEqual(symbol, "PEPE")
    
    def test_classify_balance_prompt(self):
        prompt = "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
        category = self.builder.classify_prompt(prompt)
        self.assertEqual(category, "balance")
    
    def test_classify_transactions_prompt(self):
        prompt = "List the last 10 transactions for address 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b"
        category = self.builder.classify_prompt(prompt)
        self.assertEqual(category, "transactions")
    
    def test_classify_contract_interactions_prompt(self):
        prompt = "Which addresses interacted with contract 0x6982508145454Ce325dDbE47a25d4ec3d2311933?"
        category = self.builder.classify_prompt(prompt)
        self.assertEqual(category, "contract_interactions")
    
    def test_classify_token_volume_prompt(self):
        prompt = "What's the 24-hour transfer volume of token PEPE?"
        category = self.builder.classify_prompt(prompt)
        self.assertEqual(category, "token_volume")
    
    def test_extract_ens_name(self):
        prompt = "What's the balance of vitalik.eth?"
        address = self.builder.extract_address_or_ens(prompt)
        self.assertEqual(address, "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    
    def test_extract_ens_ethereum(self):
        prompt = "Show transactions for ethereum.eth"
        address = self.builder.extract_address_or_ens(prompt)
        self.assertEqual(address, "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359")
    
    def test_classify_unknown_prompt(self):
        prompt = "What's the weather like today?"
        category = self.builder.classify_prompt(prompt)
        self.assertIsNone(category)
    
    def test_build_balance_query(self):
        prompt = "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
        query = self.builder.build_query(prompt)
        self.assertIsNotNone(query)
        self.assertEqual(query['endpoint'], 'wallet_balance')
        self.assertEqual(query['method'], 'GET')
        self.assertEqual(query['params']['address'], '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b')
        self.assertEqual(query['params']['chain'], 'eth')
    
    def test_build_transactions_query(self):
        prompt = "List the last 10 transactions for address 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b"
        query = self.builder.build_query(prompt)
        self.assertIsNotNone(query)
        self.assertEqual(query['endpoint'], 'wallet_history')
        self.assertEqual(query['params']['limit'], 10)
    
    def test_build_token_volume_query(self):
        prompt = "What's the 24-hour transfer volume of token PEPE?"
        query = self.builder.build_query(prompt)
        self.assertIsNotNone(query)
        self.assertEqual(query['endpoint'], 'token_transfers')
        self.assertEqual(query['params']['contract_address'], '0x6982508145454Ce325dDbE47a25d4ec3d2311933')
    
    def test_build_query_no_match(self):
        prompt = "What's the weather like today?"
        query = self.builder.build_query(prompt)
        self.assertIsNone(query)
    
    def test_get_token_address(self):
        pepe_address = self.builder.get_token_address('PEPE')
        self.assertEqual(pepe_address, '0x6982508145454Ce325dDbE47a25d4ec3d2311933')
        
        usdc_address = self.builder.get_token_address('USDC')
        self.assertEqual(usdc_address, '0xA0b86a33E6441b8C4505B4afDcA7FBf074497C23')
        
        unknown_address = self.builder.get_token_address('UNKNOWN')
        self.assertEqual(unknown_address, '')

if __name__ == '__main__':
    unittest.main()
