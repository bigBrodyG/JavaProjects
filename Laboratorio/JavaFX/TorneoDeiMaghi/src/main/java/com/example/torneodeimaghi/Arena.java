package com.example.torneodeimaghi;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class Arena {
    private List<Wizard> wizards;
    private Random random = new Random();
    private int turn = 0;

    public Arena(List<Wizard> wizards) {
        this.wizards = wizards;
    }

    public void playMatch() {
        while (getAliveWizards().size() > 1) {
            playTurn();
        }
        System.out.println("\n" + getWinner().getName() + " is the winner!");
    }

    public void playTurn() {
        turn++;
        System.out.println("\n----- TURNO " + turn + " -----");
        List<Wizard> aliveWizards = getAliveWizards();
        aliveWizards.sort(Comparator.comparingInt(Wizard::getSpeed).reversed());

        for (Wizard currentWizard : aliveWizards) {
            if (currentWizard.isAlive()) {
                System.out.println("\nTurno di " + currentWizard.getName() + ". " + currentWizard);
                
                List<Wizard> possibleTargets = getAliveWizards().stream()
                        .filter(w -> !w.equals(currentWizard))
                        .collect(Collectors.toList());

                if (possibleTargets.isEmpty()) {
                    break;
                }

                // AI Logic
                performAIAction(currentWizard, possibleTargets);
            }
        }
    }

    private void performAIAction(Wizard wizard, List<Wizard> targets) {
        // Priority 1: Heal if HP is critically low (< 30%)
        if (wizard.getHp() < wizard.getHpMax() * 0.3) {
            Spell healSpell = getHealSpell(wizard);
            if (healSpell != null && wizard.canCast(healSpell)) {
                wizard.cast(healSpell, wizard);
                return;
            }
        }

        // Priority 2: Attack strongest opponent
        if (targets.size() > 0) {
            Spell attackSpell = getAttackSpell(wizard);
            if (attackSpell != null && wizard.canCast(attackSpell)) {
                // Target the wizard with highest remaining HP
                Wizard strongestTarget = targets.stream()
                        .max(Comparator.comparingInt(Wizard::getHp))
                        .orElse(targets.get(0));
                wizard.cast(attackSpell, strongestTarget);
                return;
            }
        }

        // Priority 3: Heal if HP is moderate (< 60%)
        if (wizard.getHp() < wizard.getHpMax() * 0.6) {
            Spell healSpell = getHealSpell(wizard);
            if (healSpell != null && wizard.canCast(healSpell)) {
                wizard.cast(healSpell, wizard);
                return;
            }
        }

        // Priority 4: Rest to recover mana
        wizard.rest();
    }

    private Spell getAttackSpell(Wizard wizard) {
        return wizard.getSpellBook().stream()
                .filter(s -> "ATTACK".equals(s.getType()))
                .max(Comparator.comparingInt(Spell::getBaseValue))
                .orElse(null);
    }

    private Spell getHealSpell(Wizard wizard) {
        return wizard.getSpellBook().stream()
                .filter(s -> "HEAL".equals(s.getType()))
                .max(Comparator.comparingInt(Spell::getBaseValue))
                .orElse(null);
    }

    public List<Wizard> getAliveWizards() {
        return wizards.stream().filter(Wizard::isAlive).collect(Collectors.toList());
    }

    public List<Wizard> getAllWizards() {
        return wizards;
    }

    public Wizard getWinner() {
        return getAliveWizards().get(0);
    }

    public int getTurn() {
        return turn;
    }
}
