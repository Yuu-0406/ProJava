public abstract class Animal{
    private String name;

    public Animal(String name){
        this.name = name;
    }

    public abstract void naku();

    public String getName(){
        return name;
    }
}