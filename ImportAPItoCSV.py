import pandas as pd
import requests
import os

class UserAPI:    
    def __init__(self, results_count, filename_csv):
        self.results_count = results_count
        self.filename_csv = filename_csv
    
    def data_capture(self):
        try:
            response = requests.get(f'https://randomuser.me/api?results={self.results_count}')
            response.raise_for_status()
            results = response.json()['results']
            return results
        except requests.exceptions.HTTPError as e:
            print(f'Erro ao obter dados: {e}')
            return None
        except IOError as e:
            print(f'Erro ao guardar dados: {e}')
            return None 
        
    def validade_file(self):    
        if os.path.isfile(self.filename_csv):
            print("O arquivo existe!")
            return True
        else:
            print("O arquivo não existe!")
            return False
           
    def get_users(self):
        # Obtem os usuários da API
        users = self.data_capture()

        # Cria um DataFrame com as informações dos usuários
        user_data = pd.DataFrame(map(lambda user: {
            'first_name': user['name']['first'],
            'last_name': user['name']['last'],
            'email': user['email'],
            'phone': user['phone'],
            'city': user['location']['city'],
            'state': user['location']['state'],
            'country': user['location']['country']
        }, users))
            
        file_exists = self.validade_file()    
        
        if not file_exists:
            try:     
                # Salva o DataFrame como um arquivo CSV.
                user_data.to_csv(path_or_buf=self.filename_csv, mode="a+", index=False)
                print(f'Dados dos usuários salvos em {self.filename_csv} com sucesso.')    
            except requests.exceptions.HTTPError as e:
                print(f'Erro ao obter usuários: {e}')
                return None
            except IOError as e:
                print(f'Erro ao escrever no arquivo: {e}')
                return e
                
        if file_exists:
            try:
                # Carrega o arquivo CSV já existente em um DataFrame
                df = pd.read_csv(self.filename_csv)                         
                # Adiciona os dados dos usuários novos no DataFrame
                user_data = pd.concat([df, user_data], ignore_index=True)  
                # Salva o DataFrame como um arquivo CSV, adicionando ao arquivo existente, caso exista
                user_data.to_csv(path_or_buf=self.filename_csv, mode="w", index=False)
                print(f'Dados dos usuários salvos em {self.filename_csv} com sucesso.')      
            except requests.exceptions.HTTPError as e:
                print(f'Erro ao obter usuários: {e}')
                return None
            except IOError as e:
                print(f'Erro ao escrever no arquivo: {e}')
                return

if __name__ == '__main__':
    results_count = 1
    filename_csv= 'C:/Users/Jéssica/Documents/Estudo/Python/01-LeituraAPI_ImportCSV/base_dados.csv'
    api = UserAPI(results_count, filename_csv)
    api.get_users()

