public class Libro {
    private static final String BOOK_DETAILS_FORMAT = "\n----------------\nTitolo: %s\nAutore: %s\n----------------------------\n";
    private String titolo;
    private String autore;
    private int numeroPagine;
    private double costoPagina;
    final private double COSTO_FISSO = 5.5;
    
    public Libro(String titolo, String autore, int numeroPagine) {
        this.titolo = titolo;
        this.autore = autore;
        this.numeroPagine = numeroPagine;
    }
    
    public Libro(Libro libro) {
        this.titolo = libro.titolo;
        this.autore = libro.autore;
        this.numeroPagine = libro.numeroPagine;
        this.costoPagina = libro.costoPagina;
    }

    public String getTitolo() {
        return titolo;
    }
    
    public void setTitolo(String titolo) {
        this.titolo = titolo;
    }
    
    public String getAutore() {
        return autore;
    }
    
    public void setAutore(String autore) {
        this.autore = autore;
    }
    
    public int getNumeroPagine() {
        return numeroPagine;
    }
    
    public void setNumeroPagine(int numeroPagine) {
        this.numeroPagine = numeroPagine;
    }
    
    public double getCostoPagina() {
        return costoPagina;
    }
    
    public void setCostoPagina(double costoPagina) {
        this.costoPagina = costoPagina;
    }

    public double prezzo() {
        return costoPagina * numeroPagine + COSTO_FISSO;
    }
    public static void main(String[] args) throws Exception {
        Libro l1 = new Libro("How to get AURA", "giordii.dev", 120);
        l1.setCostoPagina(0.10);

        Libro l2 = new Libro("Gasa", "per dio", 1500);
        System.out.printf(BOOK_DETAILS_FORMAT, l1.getTitolo(), l1.getAutore());
        l2.setTitolo("Gasa - per dio");
        System.out.printf(BOOK_DETAILS_FORMAT, l2.getTitolo(), l2.getAutore());
        l2.setAutore("dentro");
        System.out.printf(BOOK_DETAILS_FORMAT, l2.getTitolo(), l2.getAutore());
        l2.setCostoPagina(0.15);
        System.out.printf(BOOK_DETAILS_FORMAT, l2.getTitolo(), l2.getAutore());
        l2.setAutore("aura");
        System.out.printf(BOOK_DETAILS_FORMAT, l2.getTitolo(), l2.getAutore());
        System.out.println("Prezzo l2: " + l2.prezzo());
        System.out.println("Prezzo l1: " + l1.prezzo());
        
    }
}
