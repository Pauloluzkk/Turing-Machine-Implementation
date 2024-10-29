import json


def carregar_configuracoes(arquivo_json):
    with open(arquivo_json, 'r') as file: 
        return json.load(file) 


class TuringMachine:
    
    def __init__(self, initial, final, white, transitions):
        self.estado_atual = initial  
        self.estados_finais = set(final)  
        self.simbolo_branco = white  
        
        self.transitions = {(t['from'], t['read']): (t['to'], t['write'], t['dir']) for t in transitions}
        self.fita = []  
        self.cabeca_leitura = 0  

    
    def get_palavra_atualizada(self):
        return ''.join(self.fita)

    
    def reset_fita(self, entrada):
        self.fita = list(entrada) + [self.simbolo_branco] 
        self.cabeca_leitura = 0

    
    def executar(self, entrada):
        self.reset_fita(entrada) 
        while True:  
            
            simbolo_atual = self.fita[self.cabeca_leitura] if self.cabeca_leitura < len(self.fita) else self.simbolo_branco
            
            transicao = self.transitions.get((self.estado_atual, simbolo_atual))
            if transicao:  
                to, write, dir = transicao
                self.fita[self.cabeca_leitura] = write  
                self.estado_atual = to  
               
                if dir == 'R':
                    self.cabeca_leitura += 1
                    if self.cabeca_leitura == len(self.fita):
                        self.fita.append(self.simbolo_branco)
                else:
                    self.cabeca_leitura = max(0, self.cabeca_leitura - 1)
            else:
                break  
        return self.estado_atual in self.estados_finais


def ler_entrada(arquivo_entrada):
    with open(arquivo_entrada, 'r') as file:
        return file.read().strip()


def salvar_saida(arquivo_saida, palavra_atualizada):
    with open(arquivo_saida, 'w') as file:
        file.write(palavra_atualizada)

if __name__ == "__main__":
    
    configuracoes = carregar_configuracoes("duplobal.json")
    tm = TuringMachine(configuracoes['initial'], configuracoes['final'], configuracoes['white'], configuracoes['transitions'])

    entrada = ler_entrada("Entrada_TM.txt")
    aceita = tm.executar(entrada)
    palavra_atualizada = tm.get_palavra_atualizada()

    salvar_saida("resultado_TM.txt", palavra_atualizada)
    print(f"{'1' if aceita else '0'}") 