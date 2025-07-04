base_query_rca = """
SELECT
    codsupervisor, codusur, INITCAP(nome) AS Nome, bloqueio,
    CASE
        WHEN pcusuari.codusur IN (2574, 2738, 654, 647, 2581, 712, 758, 1809, 1479, 2546, 582, 2527, 1264, 530, 649, 651, 686, 1496, 1790, 1901) THEN 'TLV'
        WHEN pcusuari.codusur IN (2629, 1572, 2144, 3057, 3018) THEN 'RDS_RCA'
        WHEN pcusuari.codusur IN (2798, 2966, 3044, 3017, 2814, 2915) THEN 'RDS_CLT'
        ELSE 'RCA'
    END AS tipo,
    CASE
        WHEN pcusuari.codusur IN (712, 758, 2738, 647, 654, 686, 582, 1496, 2527, 530, 649, 651, 1790, 1901) THEN 'Apoio'
        WHEN pcusuari.codusur IN (1809, 1479, 2581, 2546, 1264) THEN 'Televendas'
        ELSE 'Omega'
    END AS time
FROM pcusuari
"""

query_rca_todos = f"{base_query_rca} ORDER BY codsupervisor DESC"
query_rca_ativos = f"{base_query_rca} WHERE bloqueio = 'N' ORDER BY codsupervisor DESC"
query_rca_inativos = f"{base_query_rca} WHERE bloqueio = 'S' ORDER BY codsupervisor DESC"


base_query_supervisores = """
SELECT
    codgerente,
    codsupervisor,
    CASE 
        WHEN pcsuperv.codsupervisor = 22 THEN 'Elizangela'
        WHEN pcsuperv.codsupervisor = 34 THEN 'Atac - Marlon'
        ELSE INITCAP(REGEXP_SUBSTR(pcsuperv.nome, '^[^/]+'))
    END AS Supervisor,
    posicao,
    CASE 
        WHEN codsupervisor = 22 THEN 'Televendas'
        WHEN codsupervisor = 34 THEN 'Atacado'
        WHEN codsupervisor IN (29, 19, 33) THEN 'Capital'
        WHEN codsupervisor IN (35) THEN 'Cariri'
        WHEN codsupervisor IN (32, 38) THEN 'Cariri P2'
        WHEN codsupervisor IN (39, 30) THEN 'Cariri P1'
        WHEN codsupervisor IN (20, 1, 8, 23) THEN 'Interior'
        ELSE 'Outra SubRegião'
    END AS subregiao
FROM pcsuperv
"""

query_supervisores_todos = f"{base_query_supervisores} ORDER BY codgerente"
query_supervisores_ativos = f"{base_query_supervisores} WHERE posicao = 1 ORDER BY codgerente"
query_supervisores_inativos = f"{base_query_supervisores} WHERE posicao <> 1 ORDER BY codgerente"


base_query_coordenadores = """
SELECT
    codgerente,
    CASE 
        WHEN codgerente = 14 THEN 'Coord. Atacado'
        WHEN codgerente = 13 THEN 'Coord. Genildo'
        WHEN codgerente = 12 THEN 'Coord. Arleilson'
        WHEN codgerente = 10 THEN 'Coord. Marlon'
        WHEN codgerente = 9  THEN 'Coord. Geral'
        ELSE 'Coordenador'
    END AS Coordenador,
    CASE
        WHEN codgerente = 9 THEN 'Geral'
        WHEN codgerente = 13 THEN 'Cariri'
        WHEN codgerente = 12 THEN 'Capital'
        WHEN codgerente = 10 THEN 'Interior'
        WHEN codgerente = 14 THEN 'Atacado'
        ELSE 'Outra Região'
    END AS regiao
FROM pcgerente
"""

query_coordenadores_todos = f"{base_query_coordenadores} ORDER BY codgerente"
query_coordenadores_ativos = f"{base_query_coordenadores} WHERE SITUACAO = 'A' ORDER BY codgerente"
query_coordenadores_inativos = f"{base_query_coordenadores} WHERE SITUACAO = 'I' ORDER BY codgerente"