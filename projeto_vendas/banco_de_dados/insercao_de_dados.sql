-- VENDEDORES
INSERT INTO vendedores (nome) VALUES
('Pedro Moura'),
('Marcos Henrique'),
('Marcio Rodrigues'),
('Emilio');


-- PRODUTOS
INSERT INTO produtos (descricao, preco) VALUES
('Bola', 49.00),
('Album da copa', 74.90),
('Figurinhas da copa', 7.00),
('Boneco Batman', 39.90),
('LEGO Batman', 59.90),
('LEGO Hogwarts', 99.90),
('LEGO Ferrari', 129.90),
('LEGO Pikachu', 109.90),
('LEGO Taça da copa', 119.90),
('Cartas Pokemon', 15.00),
('Boneco Spiderman', 44.90),
('Smartwatch Infantil', 99.90),
('Console Retro de Bolso', 149.90),
('Controle USB para Games', 49.90),
('Carrinho de Controle Remoto', 120.00),
('Boneca Articulada', 85.00),
('Jogo de Tabuleiro', 110.00),
('Blocos de Montar 500 peças', 190.00),
('Pista de Carrinhos', 230.00),
('Videogame Portátil Infantil', 450.00),
('Mini Quadriciclo Elétrico', 1200.00),
('Urso de Pelúcia Gigante', 250.00),
('Dinossauro T-Rex com Som', 160.00),
('Drone Infantil com Câmera', 380.00),
('Bicicleta Aro 12', 420.00),
('Patinete de Alumínio', 290.00),
('Kit de Passes de Mágica', 75.00),
('Microfone Musical Infantil', 95.00),
('Playstation 5 Slim', 3900.00),
('Nintendo Switch OLED', 2200.00),
('Mesa de Pebolim/Totó', 650.00),
('Cozinha de Brinquedo Completa', 320.00),
('Massinha de Modelar Kit Luxo', 60.00),
('Cubo Mágico Profissional', 45.00),
('Quebra-Cabeça 1000 Peças', 70.00),
('Lego Star Wars', 550.00),
('Lego Harry Potter', 480.00),
('Foguete Espacial com Luz', 140.00),
('Barco de Controle Remoto', 210.00),
('Lançador de Dardos Espuma', 130.00),
('Arco e Flecha Infantil', 80.00),
('Mini Cama Elástica / Pula-Pula', 850.00),
('Piscina de Bolinhas', 400.00),
('Walkie Talkie Infantil', 115.00),
('Relógio Infantil com Jogos', 175.00),
('Ioiô Profissional de Metal', 55.00),
('Skate Completo Iniciante', 165.00),
('Projetor de Desenhos LED', 90.00),
('Teclado Musical Infantil', 240.00);


-- VENDAS
INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final) VALUES
-- Janeiro
(1, '2026-01-05 10:15:00', 5.00, 115.00),  
(2, '2026-01-10 14:30:00', 0.00, 230.00),   
(3, '2026-01-15 09:45:00', 10.00, 75.00),  
(4, '2026-01-20 16:00:00', 0.00, 190.00),   
(1, '2026-01-25 11:20:00', 15.00, 95.00),   
-- Fevereiro
(2, '2026-02-03 13:10:00', 0.00, 380.00),   
(3, '2026-02-08 15:50:00', 20.00, 270.00),  
(4, '2026-02-12 08:30:00', 0.00, 160.00),   
(1, '2026-02-18 17:25:00', 30.00, 390.00),  
(2, '2026-02-25 12:40:00', 0.00, 250.00);   



-- VENDAS PRODUTOS
INSERT INTO vendas_produtos 
(id_venda, id_produto, quantidade, valor_unitario, valor_total) 
VALUES
-- Venda 1
(1, 1, 1, 120.00, 120.00),    
(1, 6, 3, 450.00, 1350.00),   
-- Venda 2
(2, 4, 1, 190.00, 190.00),    
(2, 35, 2, 240.00, 480.00),   
-- Venda 3
(3, 2, 1, 85.00, 85.00),      
(3, 16, 3, 2200.00, 6600.00), 
(3, 17, 2, 650.00, 1300.00),  
(3, 18, 1, 320.00, 320.00),   
-- Venda 4
(4, 8, 2, 250.00, 500.00),    
-- Venda 5
(5, 10, 2, 380.00, 760.00),   
(5, 11, 2, 420.00, 840.00),   
(5, 34, 4, 90.00, 360.00),   
-- Venda 6
(6, 43, 1, 150.00, 150.00),  
(6, 41, 2, 85.00, 170.00),    
-- Venda 7
(7, 14, 1, 95.00, 95.00),     
(7, 17, 3, 650.00, 1950.00),  
-- Venda 8
(8, 23, 2, 480.00, 960.00),  
-- Venda 9
(9, 29, 2, 400.00, 800.00),   
(9, 47, 2, 65.00, 130.00),    
-- Venda 10
(10, 10, 5, 380.00, 1900.00); 
