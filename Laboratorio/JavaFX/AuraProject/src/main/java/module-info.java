module aura.auraproject {
    requires javafx.controls;
    requires javafx.fxml;


    opens aura.auraproject to javafx.fxml;
    exports aura.auraproject;
}