package edu.harvard.cs50.pokedex;

public class Pokemon {
    private String name;
    private String url;
    private Boolean caught;

    Pokemon(String name, String url, Boolean caught) {
        this.name = name;
        this.url = url;
        this.caught = caught;
    }

    public String getName() {
        return name;
    }

    public String getUrl() {
        return url;
    }

    public Boolean getCaught() { return caught; }

    public void setCaught(boolean caught) {
        this.caught = caught;
    }
}
