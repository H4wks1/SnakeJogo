# Snake Jogo
**Funcionalidades Implementadas e Características Principais** 
O jogo apresenta as seguintes funcionalidades:
1. Mecânica Horta/Fazenda: A tela utiliza um fundo e uma grade temática de horta, com a cobra se movendo em um mapa que se comporta como um torus (teleporte nas bordas).
2. Múltiplas Comidas (MAX_FOODS = 5): O jogo suporta o gerenciamento simultâneo de até 5 itens de comida na tela.
3. Sistema de Comidas Balanceado: Implementação de dois tipos de comida com diferentes efeitos:]
   - Vegetais (Laranja): 80% de chance de aparecer, aumenta a pontuação e faz a cobra crescer.
   - Fast Food (Marrom): 20% de chance de aparecer, penaliza a pontuação e encolhe o corpo da cobra.
4. Modularização (Classes e Sprites): O projeto foi estruturado para usar a arquitetura de Sprites e Grupos de Sprites do Pygame, com a criação de um módulo separado (comida.py) para gerenciar os objetos de comida (Comida ou Fruta), facilitando o uso de imagens reais (morango e hambúrguer, com fallback para cores se as imagens não estiverem disponíveis).
5. Tela de Game Over: Implementação de uma tela de fim de jogo com pontuação final e opções para reiniciar ou sair.
