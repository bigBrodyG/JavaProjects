module aura.auraapp {
    requires javafx.controls;
    requires javafx.fxml;


    opens aura.auraapp to javafx.fxml;
    exports aura.auraapp;
}