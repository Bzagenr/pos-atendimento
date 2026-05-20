from app.database import SessionLocal
from app.models.tipodoenca import TipoDoenca
from app.models.orientacao import OrientacaoPadrao
from app.models.acompanhamento import TipoMensagem, OpcaoResposta
import app.models.paciente
import app.models.consulta
import app.models.receita

db = SessionLocal()

try:
    # ── TipoDoenca ────────────────────────────────────────────────────────────
    print("Inserindo TipoDoenca...")
    doencas = [
        "Hipertensão Arterial Sistêmica",
        "Diabetes Mellitus Tipo 2",
        "Influenza (Gripe)",
        "Gastroenterite Aguda",
        "Infecção do Trato Urinário (ITU)",
        "Asma Brônquica",
        "Dislipidemia (Colesterol Alto)",
        "Hipotireoidismo",
        "Lombalgia Aguda",
        "Transtorno de Ansiedade Generalizada",
        "Doença do Refluxo Gastroesofágico",
        "Rinite Alérgica",
    ]
    for nome in doencas:
        if not db.query(TipoDoenca).filter(TipoDoenca.nome == nome).first():
            db.add(TipoDoenca(nome=nome))
    db.commit()
    print(f"✅ {len(doencas)} doenças inseridas")

    # ── OrientacaoPadrao ──────────────────────────────────────────────────────
    print("Inserindo OrientacaoPadrao...")
    orientacoes = [
        (1, "Medir a pressão arterial 2x ao dia (manhã e noite) e anotar os valores.", 30, True),
        (1, "Reduzir a ingestão de sal para menos de 5g por dia e evitar embutidos.", None, False),
        (1, "Praticar exercícios aeróbicos leves (como caminhada) por 30 min, 3x na semana.", 60, False),
        (2, "Monitorar glicemia capilar em jejum diariamente.", 15, True),
        (2, "Inspecionar os pés diariamente em busca de lesões, cortes ou vermelhidão.", None, False),
        (3, "Manter repouso e hidratação vigorosa (pelo menos 2,5L de água/dia).", None, False),
        (3, "Se a febre persistir por mais de 3 dias ou houver falta de ar, buscar o pronto-socorro.", 3, True),
        (4, "Tomar soro de reidratação oral após cada episódio de diarreia.", None, False),
        (4, "Observar sinais de desidratação grave (boca muito seca, ausência de urina).", 2, True),
        (5, "Tomar o antibiótico prescrito nos horários corretos até o fim, mesmo se os sintomas sumirem.", 7, True),
        (5, "Aumentar a ingestão de líquidos para ajudar na lavagem da via urinária.", None, False),
        (6, "Usar a medicação de resgate (bombinha curta) apenas se houver crise (falta de ar/chiado).", None, False),
        (6, "Avaliar a frequência de uso da bombinha de resgate na semana.", 30, True),
        (7, "Aumentar o consumo de fibras (aveia, frutas com casca) e reduzir gorduras saturadas.", 90, False),
        (7, "Repetir exames de sangue de perfil lipídico antes do próximo retorno.", 90, True),
        (8, "Tomar a medicação em jejum absoluto, aguardando 30 a 40 minutos para tomar café da manhã.", None, False),
        (8, "Repetir exame de TSH para ajustar a dose após 6 semanas de uso contínuo da medicação.", 45, True),
        (9, "Fazer compressas quentes na região lombar por 20 minutos, 3x ao dia.", None, False),
        (9, "Evitar carregar pesos e iniciar as sessões de fisioterapia recomendadas.", 15, True),
        (10, "Praticar higiene do sono, desligando telas 1h antes de deitar.", None, False),
        (10, "Agendar e iniciar o acompanhamento psicológico/terapia.", 30, True),
        (11, "Elevar a cabeceira da cama em 15 cm e evitar deitar-se até 2h após as refeições.", None, False),
        (11, "Observar se a queimação persiste mesmo com o uso contínuo do protetor gástrico diário.", 30, True),
    ]
    for idDoenca, descricao, dias, exige in orientacoes:
        if not db.query(OrientacaoPadrao).filter(OrientacaoPadrao.descricao == descricao).first():
            db.add(OrientacaoPadrao(
                idTipoDoenca=idDoenca,
                descricao=descricao,
                diasRetornoPadrao=dias,
                exigeAcompanhamento=exige
            ))
    db.commit()
    print(f"✅ {len(orientacoes)} orientações padrão inseridas")

    # ── TipoMensagem ──────────────────────────────────────────────────────────
    print("Inserindo TipoMensagem...")
    tipos_mensagem = [
        ("Lembrete de retorno", "Olá, {nome}. Você tem um retorno médico sugerido para perto do dia {data}. Gostaria de agendar agora?", True),
        ("Acompanhamento de Sintomas Agudos", "Olá, {nome}. Já se passaram alguns dias da sua consulta. Como estão os seus sintomas hoje?", True),
        ("Adesão ao Tratamento", "Olá, {nome}. Você está conseguindo seguir as orientações e tomar as medicações prescritas pelo médico?", True),
        ("Evolução de Dor", "Olá, {nome}. Em relação à queixa de dor da sua última consulta, qual o seu nível de dor atual?", True),
        ("Lembrete de Exames", "Olá, {nome}. Este é um lembrete para realizar seus exames laboratoriais até {data} para estarem prontos no retorno.", False),
        ("Monitoramento de Sinais Vitais", "Olá, {nome}. As suas medições feitas em casa (pressão/glicemia) estão dentro dos limites orientados?", True),
        ("Pesquisa de Satisfação", "Olá, {nome}. Gostaríamos muito de saber como foi a sua experiência no atendimento clínico do dia {data}.", True),
        ("Instrução de Cuidado", "Olá, {nome}. Lembre-se sempre de manter uma boa hidratação e seguir o plano de cuidados. Conte conosco!", False),
        ("Alerta de Efeitos Colaterais", "Olá, {nome}. Notou algum efeito colateral intenso ou desconforto inesperado após iniciar a medicação?", True),
        ("Conclusão de Tratamento", "Olá, {nome}. O período estimado do seu tratamento agudo finalizou em {data}. Você se sente totalmente recuperado(a)?", True),
    ]
    for nome, template, aceita in tipos_mensagem:
        if not db.query(TipoMensagem).filter(TipoMensagem.nome == nome).first():
            db.add(TipoMensagem(nome=nome, template=template, aceitaResposta=aceita))
    db.commit()
    print(f"✅ {len(tipos_mensagem)} tipos de mensagem inseridos")

    # ── OpcaoResposta ─────────────────────────────────────────────────────────
    print("Inserindo OpcaoResposta...")
    opcoes = [
        (1, "Sim, quero agendar", 1),
        (1, "Não, já agendei", 2),
        (1, "Não vou retornar no momento", 3),
        (2, "Melhoraram bastante", 1),
        (2, "Estão iguais", 2),
        (2, "Pioraram", 3),
        (3, "Estou seguindo perfeitamente", 1),
        (3, "Tive dificuldades / Esqueci algumas vezes", 2),
        (3, "Não consegui comprar a medicação / Parei", 3),
        (4, "Sem dor / Alívio total", 1),
        (4, "Dor leve e suportável", 2),
        (4, "Dor moderada a intensa", 3),
        (6, "Sim, estão normais / controlados", 1),
        (6, "Tive algumas alterações pontuais", 2),
        (6, "Muito alterados / Fora do controle", 3),
        (7, "Muito satisfeito", 1),
        (7, "Satisfeito", 2),
        (7, "Insatisfeito / Tive problemas", 3),
        (9, "Não, tudo ótimo", 1),
        (9, "Sim, mas são leves e toleráveis", 2),
        (9, "Sim, estou passando mal / Preciso de ajuda", 3),
        (10, "Sim, 100% recuperado(a)", 1),
        (10, "Parcialmente, ainda sinto alguns incômodos", 2),
        (10, "Não, os sintomas continuam fortes", 3),
    ]
    for idTipo, descricao, ordem in opcoes:
        if not db.query(OpcaoResposta).filter(OpcaoResposta.descricao == descricao).first():
            db.add(OpcaoResposta(idTipoMensagem=idTipo, descricao=descricao, ordem=ordem))
    db.commit()
    print(f"✅ {len(opcoes)} opções de resposta inseridas")

    print("\n✅ Seed concluído com sucesso!")

except Exception as e:
    db.rollback()
    print(f"❌ Erro: {e}")
finally:
    db.close()
