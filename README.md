# Projeto de Ray Tracing

Este projeto é uma implementação de um Ray Tracer simples em Python. O Ray Tracing é uma técnica de renderização que simula a forma como a luz interage com os objetos em uma cena para produzir imagens realistas. O projeto foi inspirado em um exemplo de Ray Tracing do professor Claudio Esperança (https://observablehq.com/@esperanc/raytracing).

## Descrição

Este Ray Tracer foi desenvolvido para renderizar uma cena composta por esferas e um plano, com suporte para iluminação ambiente, difusa e especular, bem como reflexões. A câmera está posicionada em um ponto fixo, olhando diretamente para a cena. A fonte de luz é colocada em uma posição fixa acima e atrás da câmera.

### Decisões de Projeto

#### 1. Linguagem e Bibliotecas:
      - A implementação foi feita em Python, utilizando as bibliotecas numpy para operações matemáticas e matplotlib para a geração e salvamento da imagem renderizada.

#### 2. Objetos na Cena:
      - A cena é composta por três esferas e um plano. As esferas menores estão flutuando acima do plano, enquanto a esfera maior está centralizada e mais ao fundo.
      - As posições, tamanhos e cores das esferas foram ajustadas para diferenciar esta implementação da referência original.

#### 3. Iluminação:
      - A iluminação inclui componentes ambiente, difusa e especular, simulando a forma como a luz interage com as superfícies dos objetos.
      - A fonte de luz está posicionada acima e atrás da câmera para criar sombras e reflexões realistas.
#### 4. Reflexões:
      - As esferas possuem propriedades reflexivas, permitindo a visualização de reflexos umas nas outras e no plano.
      - Foi utilizado um limite máximo de recursão de 3 para evitar cálculos excessivos e melhorar o desempenho.

## Estrutura do Código

#### 1. Funções de Interseção:
      - intersect_sphere: Calcula a interseção do raio com uma esfera.
      - intersect_plane: Calcula a interseção do raio com um plano.

#### 2. Funções Auxiliares:
      - find_closest_object: Encontra o objeto mais próximo que o raio intersecta.
      - normalize: Normaliza um vetor.
      - reflect: Calcula a reflexão de um vetor em relação a um eixo.

#### 3. Função Principal de Ray Tracing:
      - ray_tracing: Realiza o traçado do raio, calculando as interseções e a iluminação para determinar a cor final do pixel.

#### 4. Renderização da Cena:
      - O loop principal percorre todos os pixels da imagem, calculando a cor de cada um com base nas interseções dos raios com os objetos da cena.

## Como Executar

Para executar o projeto, certifique-se de ter as bibliotecas numpy e matplotlib instaladas. Você pode instalá-las usando pip:
pip install numpy matplotlib

Em seguida, execute o script principal para gerar a imagem:
python ray_tracing.py

A imagem renderizada será salva como ray_tracing_spheres.png.

## Melhorias Futuras

  - Adicionar suporte para mais tipos de objetos (cilindros, cones, etc.).
  - Implementar mais efeitos de iluminação, como transparência e refração.
  - Otimizar o código para melhorar o desempenho em cenas mais complexas.
