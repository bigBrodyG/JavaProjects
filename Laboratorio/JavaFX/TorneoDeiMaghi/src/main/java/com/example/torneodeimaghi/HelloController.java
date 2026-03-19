package com.example.torneodeimaghi;

import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.layout.VBox;
import javafx.util.Duration;

import java.io.PrintStream;
import java.util.*;

public class HelloController {
    @FXML
    private Button startButton;
    @FXML
    private Button pauseButton;
    @FXML
    private Button resetButton;
    @FXML
    private Label speedLabel;
    @FXML
    private Label speedValue;
    @FXML
    private TextArea logArea;
    @FXML
    private VBox wizardsContainer;
    @FXML
    private Label resultLabel;

    private Arena arena;
    private List<Wizard> wizards;
    private boolean isSimulating = false;
    private boolean isPaused = false;
    private int simulationSpeed = 1; // 1x, 2x, 4x

    private StringBuilder logBuffer;
    private PrintStream logStream;

    @FXML
    public void initialize() {
        logBuffer = new StringBuilder();
        logStream = new PrintStream(System.out) {
            @Override
            public void println(String x) {
                super.println(x);
                Platform.runLater(() -> {
                    logBuffer.append(x).append("\n");
                    logArea.appendText(x + "\n");
                    logArea.setScrollTop(Double.MAX_VALUE);
                });
            }
        };
        
        System.setOut(logStream);
        initializeWizards();
    }

    private void initializeWizards() {
        wizards = new ArrayList<>();
        Random random = new Random();

        String[] names = {"Merlino", "Morgana", "Gandalf", "Saruman", "Circe", "Medea", "Merlin", "Nimue"};
        String[] aliases = {"Mago Blu", "Maga Oscura", "Grigio", "Bianco", "Strega", "Maga del Mare", "Saggio", "Gaia"};

        for (int i = 0; i < 4; i++) {
            int hp = random.nextInt(21) + 40;        // 40-60
            int mana = random.nextInt(21) + 20;      // 20-40
            int magicPower = random.nextInt(6) + 5;  // 5-10
            int defense = random.nextInt(6) + 3;     // 3-8
            int speed = random.nextInt(10) + 1;      // 1-10

            List<Spell> spellBook = new ArrayList<>();
            spellBook.add(new Spell("Fulmine", 7, 10, "ATTACK"));
            spellBook.add(new Spell("Palla di Fuoco", 9, 12, "ATTACK"));
            spellBook.add(new Spell("Cura", 6, 8, "HEAL"));
            spellBook.add(new Spell("Guarigione Maggiore", 10, 15, "HEAL"));

            Wizard wizard = new Wizard(names[i], aliases[i], hp, mana, magicPower, defense, speed, spellBook);
            wizards.add(wizard);
        }

        arena = new Arena(wizards);
        updateWizardsDisplay();
    }

    @FXML
    protected void onStartSimulation() {
        if (isSimulating) return;

        isSimulating = true;
        isPaused = false;
        startButton.setDisable(true);
        pauseButton.setDisable(false);
        resetButton.setDisable(true);
        logArea.clear();
        resultLabel.setText("");

        Thread simulationThread = new Thread(this::runSimulation);
        simulationThread.setDaemon(true);
        simulationThread.start();
    }

    @FXML
    protected void onPauseSimulation() {
        isPaused = !isPaused;
        if (isPaused) {
            pauseButton.setText("▶ Riprendi");
        } else {
            pauseButton.setText("⏸ Pausa");
        }
    }

    @FXML
    protected void onResetSimulation() {
        isSimulating = false;
        isPaused = false;
        logArea.clear();
        resultLabel.setText("");
        startButton.setDisable(false);
        pauseButton.setDisable(true);
        pauseButton.setText("⏸ Pausa");
        resetButton.setDisable(false);
        initializeWizards();
    }

    private void runSimulation() {
        int turnCount = 0;
        
        while (arena.getAliveWizards().size() > 1 && isSimulating) {
            // Check if paused
            while (isPaused && isSimulating) {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }

            if (!isSimulating) break;

            turnCount++;
            arena.playTurn();
            updateWizardsDisplay();

            // Calculate delay based on speed
            long delayMs = switch (simulationSpeed) {
                case 2 -> 500;
                case 4 -> 250;
                default -> 1000;
            };

            try {
                Thread.sleep(delayMs);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        // Match finished
        if (isSimulating) {
            isSimulating = false;
            Wizard winner = arena.getWinner();
            Platform.runLater(() -> {
                resultLabel.setText("🏆 VINCITORE: " + winner.getName() + " (" + winner.getAlias() + ") con " + winner.getHp() + " HP rimasti!");
                startButton.setDisable(false);
                pauseButton.setDisable(true);
                resetButton.setDisable(false);
                pauseButton.setText("⏸ Pausa");
            });
        }
    }

    private void updateWizardsDisplay() {
        Platform.runLater(() -> {
            wizardsContainer.getChildren().clear();
            
            for (Wizard wizard : wizards) {
                Label wizardLabel = createWizardLabel(wizard);
                wizardsContainer.getChildren().add(wizardLabel);
            }
        });
    }

    private Label createWizardLabel(Wizard wizard) {
        String status = wizard.isAlive() ? "✓ Vivo" : "✗ Morto";
        String text = String.format("%s (%s) - %s | HP: %d/%d | Mana: %d/%d | Difesa: %d | Velocità: %d",
                wizard.getName(),
                wizard.getAlias(),
                status,
                wizard.getHp(),
                wizard.getHpMax(),
                wizard.getMana(),
                wizard.getManaMax(),
                wizard.getDefense(),
                wizard.getSpeed());

        Label label = new Label(text);
        if (!wizard.isAlive()) {
            label.setStyle("-fx-text-fill: #cc0000;");
        } else {
            label.setStyle("-fx-text-fill: #00aa00;");
        }
        label.setStyle(label.getStyle() + "; -fx-font-family: 'Consolas'; -fx-font-size: 10;");
        return label;
    }
}
