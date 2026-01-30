#!/usr/bin/env python3
"""
Solução para o Problema do Jantar dos Filósofos

Requisitos:
1. O processamento dos filósofos devem ser threads em 1 único processo
2. São 5 filósofos sentados a mesa
3. Antes de comer, o filósofo deve pegar 2 talheres
4. Após comer, o filósofo devolve os talheres a mesa
5. Como os palitos são compartilhados, 2 filósofos vizinhos não podem comer ao mesmo tempo
6. Os filósofos não conversam entre si, nem conhecem os estados uns dos outros
7. Não há um coordenador central
"""

import threading
import time
import random


class Filosofo(threading.Thread):
    """
    Representa um filósofo que pensa e come.
    Cada filósofo é uma thread independente.
    """
    
    def __init__(self, philosopher_id, talher_esquerdo, talher_direito, max_refeicoes=3):
        """
        Inicializa um filósofo.
        
        Args:
            philosopher_id: Identificador do filósofo (0-4)
            talher_esquerdo: Lock representando o talher à esquerda
            talher_direito: Lock representando o talher à direita
            max_refeicoes: Número máximo de refeições (padrão: 3)
        """
        super().__init__()
        self.philosopher_id = philosopher_id
        self.talher_esquerdo = talher_esquerdo
        self.talher_direito = talher_direito
        self.refeicoes = 0
        self.max_refeicoes = max_refeicoes
        
    def pensar(self):
        """Filósofo está pensando."""
        print(f"Filósofo {self.philosopher_id} está pensando...")
        time.sleep(random.uniform(0.1, 0.5))
        
    def pegar_talheres(self):
        """
        Filósofo tenta pegar os dois talheres.
        Para evitar deadlock, os filósofos ímpares pegam primeiro o talher direito.
        """
        if self.philosopher_id % 2 == 0:
            # Filósofos pares pegam primeiro o talher esquerdo
            primeiro_talher = self.talher_esquerdo
            segundo_talher = self.talher_direito
        else:
            # Filósofos ímpares pegam primeiro o talher direito
            primeiro_talher = self.talher_direito
            segundo_talher = self.talher_esquerdo
            
        primeiro_talher.acquire()
        print(f"Filósofo {self.philosopher_id} pegou o primeiro talher")
        
        try:
            segundo_talher.acquire()
            print(f"Filósofo {self.philosopher_id} pegou o segundo talher")
        except:
            # Se falhar ao pegar o segundo talher, libera o primeiro
            primeiro_talher.release()
            raise
        
    def comer(self):
        """Filósofo está comendo."""
        print(f"Filósofo {self.philosopher_id} está comendo (refeição {self.refeicoes + 1}/{self.max_refeicoes})")
        time.sleep(random.uniform(0.2, 0.6))
        self.refeicoes += 1
        
    def devolver_talheres(self):
        """Filósofo devolve os dois talheres à mesa."""
        self.talher_direito.release()
        print(f"Filósofo {self.philosopher_id} devolveu o talher direito")
        
        self.talher_esquerdo.release()
        print(f"Filósofo {self.philosopher_id} devolveu o talher esquerdo")
        
    def run(self):
        """
        Execução da thread do filósofo.
        Ciclo: pensar -> pegar talheres -> comer -> devolver talheres
        """
        print(f"Filósofo {self.philosopher_id} sentou-se à mesa")
        
        try:
            while self.refeicoes < self.max_refeicoes:
                self.pensar()
                self.pegar_talheres()
                try:
                    self.comer()
                finally:
                    self.devolver_talheres()
        except Exception as e:
            print(f"Filósofo {self.philosopher_id} encontrou um erro: {e}")
            raise
        finally:
            print(f"Filósofo {self.philosopher_id} terminou de comer e saiu da mesa")


def jantar_dos_filosofos():
    """
    Simula o jantar dos filósofos.
    Cria 5 filósofos e 5 talheres (locks).
    """
    NUM_FILOSOFOS = 5
    
    # Cria os talheres (locks) - um entre cada par de filósofos
    talheres = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
    
    # Cria os filósofos como threads
    # Cada filósofo tem acesso ao talher à sua esquerda e à sua direita
    filosofos = []
    for i in range(NUM_FILOSOFOS):
        talher_esquerdo = talheres[i]
        talher_direito = talheres[(i + 1) % NUM_FILOSOFOS]
        filosofo = Filosofo(i, talher_esquerdo, talher_direito)
        filosofos.append(filosofo)
    
    print("=" * 50)
    print("Iniciando o Jantar dos Filósofos")
    print("=" * 50)
    
    # Inicia todas as threads dos filósofos
    for filosofo in filosofos:
        filosofo.start()
    
    # Aguarda todas as threads terminarem
    for filosofo in filosofos:
        filosofo.join()
    
    print("=" * 50)
    print("Jantar dos Filósofos finalizado!")
    print("=" * 50)


if __name__ == "__main__":
    jantar_dos_filosofos()
