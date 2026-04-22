# Copilot CLI Instructions

Instruções customizadas para workflows do Copilot CLI neste projeto.

## ⚠️ Gestão de Tickets no Jira

**NUNCA** criar, alterar ou apagar tickets no Jira sem **revisão prévia do usuário**.

**Regra:** Sempre solicitar aprovação do usuário antes de qualquer operação no Jira (criação de issues, mudança de status, comentários, etc).

**Exceção:** Apenas operações de leitura (consultar, listar issues) são permitidas sem revisão.

## Workflow de Issues e Pull Requests

### Status de Issues no Jira

Seguimos um workflow de 3 estados para rastrear o progresso:

```
To Do → In Review → Done
```

### Regras de Transição

#### 1. **To Do** → **In Review**
- **Quando:** Assim que uma task é resolvida/implementada (código pronto, testes passando)
- **Ação:** Transicionar a issue para "In Review" no Jira
- **Próximo passo:** Aguardar PR review e merge

#### 2. **In Review** → **Done**
- **Quando:** APENAS após o PR ser mergeado para a branch principal
- **Ação:** Transicionar a issue para "Done" no Jira
- **Nota:** Nunca colocar direto em "Done" sem PR mergeado

### Processo Completo

1. **Desenvolvimento**
   - Pegar issue em "To Do"
   - Implementar solução
   - Adicionar/atualizar testes
   - Validar que testes passam

2. **Resolução (Transição para In Review)**
   ```
   Jira Transition: SCRUM-X → In Review
   Ação do Copilot: 
     - Transicionar issue para "In Review"
     - Adicionar comentário com resumo da solução
   ```

3. **Code Review**
   - Abrir PR no GitHub (se aplicável)
   - Solicitar review
   - Aguardar feedback

4. **Merge & Closure (Transição para Done)**
   ```
   Após PR mergeado:
   Jira Transition: SCRUM-X → Done
   ```

### Exemplo de Fluxo (SCRUM-4)

```
1. Início: SCRUM-4 está em "To Do"
2. Desenvolvimento: Corrigir bug em books.py
3. Testes: Adicionar testes + validar (9/9 passing ✓)
4. Resolução: Transicionar para "In Review"
   └─ Comentário: "Bug resolvido. Aguardando merge do PR."
5. GitHub: PR aberto, reviewed e mergeado
6. Closure: Transicionar para "Done"
```

## Convenções de Commit

- Usar commits convencionais (feat:, fix:, test:, docs:)
- Incluir sempre o trailer: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`

Exemplo:
```
fix: partial author name search in book-app-project

- Use substring matching instead of exact comparison
- Add support for case-insensitive search
- Add 4 new test cases

Closes SCRUM-4

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

## Comunicação em Jira

### Ao Resolver Uma Issue

Adicionar comentário com:
- ✅ Breve resumo da solução
- 📝 Mudanças principais
- ✨ Recursos/correções adicionadas
- 🧪 Status dos testes
- 🔗 Links para código/branch (se aplicável)

### Ao Transicionar Para In Review

Template:
```
✅ **Resolvido e pronto para review**

**Mudanças:**
- [Lista de mudanças]

**Testes:**
- [Status dos testes]

**Status:** ✅ Aguardando PR merge
```

## Checklist Para Completar Uma Task

- [ ] Código implementado
- [ ] Testes escritos/atualizados
- [ ] Todos os testes passando
- [ ] Código revisado (verificar style, type hints, etc)
- [ ] Comentários descritivos no Jira adicionados
- [ ] **Issue transicionada para "In Review"** ← IMPORTANTE!
- [ ] PR aberto (se aplicável)
- [ ] Aguardar merge
- [ ] Após merge: transicionar para "Done"

## Notas Importantes

⚠️ **NUNCA:**
- Colocar diretamente em "Done" sem PR mergeado
- Pular a etapa "In Review"
- Esquecer de atualizar o comentário no Jira
- **Criar, alterar ou apagar tickets no Jira sem revisão prévia** ← CRÍTICO!

✅ **SEMPRE:**
- Validar testes antes de transicionar
- Documentar a solução em comentário no Jira
- Aguardar conclusão do workflow (merge do PR)
