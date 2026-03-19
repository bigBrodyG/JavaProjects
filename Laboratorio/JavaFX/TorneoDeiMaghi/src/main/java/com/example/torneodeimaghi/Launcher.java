package com.example.torneodeimaghi;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Launcher - Versione Console della Simulazione Arena dei Maghi
 * 
 * Per eseguire la versione GUI:
 *   mvn javafx:run
 * 
 * Per eseguire la versione Console:
 *   mvn compile exec:java -Dexec.mainClass="com.example.torneodeimaghi.Launcher"
 */
public class Launcher {
    public static void main(String[] args) {
        System.out.println("════════════════════════════════════════════════════════════");
        System.out.println("         🧙 ARENA DEI MAGHI - SIMULAZIONE FREE-FOR-ALL 🧙");
        System.out.println("════════════════════════════════════════════════════════════\n");
        
        Random random = new Random();

        // Create Spells
        List<Spell> spellBook = createSpellBook();

        // Create Wizards with random stats
        List<Wizard> wizards = new ArrayList<>();
        String[] names = {"Merlino", "Morgana", "Gandalf", "Saruman"};
        String[] aliases = {"Mago Blu", "Maga Oscura", "Grigio", "Bianco"};

        for (int i = 0; i < names.length; i++) {
            int hp = random.nextInt(21) + 40;        // HP: 40-60
            int mana = random.nextInt(21) + 20;      // Mana: 20-40
            int magicPower = random.nextInt(6) + 5;  // Magic Power: 5-10
            int defense = random.nextInt(6) + 3;     // Defense: 3-8
            int speed = random.nextInt(10) + 1;      // Speed: 1-10

            Wizard wizard = new Wizard(names[i], aliases[i], hp, mana, magicPower, defense, speed, spellBook);
            wizards.add(wizard);
            System.out.println("✓ " + wizard);
        }

        System.out.println("\n════════════════════════════════════════════════════════════\n");
        System.out.println("Inizio della simulazione...\n");

        // Start the Arena
        Arena arena = new Arena(wizards);
        arena.playMatch();
    }

    private static List<Spell> createSpellBook() {
        List<Spell> spells = new ArrayList<>();
        spells.add(new Spell("Fulmine", 7, 10, "ATTACK"));
        spells.add(new Spell("Palla di Fuoco", 9, 12, "ATTACK"));
        spells.add(new Spell("Cura", 6, 8, "HEAL"));
        spells.add(new Spell("Guarigione Maggiore", 10, 15, "HEAL"));
        return spells;
    }
}
