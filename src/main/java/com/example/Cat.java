public class Cat extends Animal{
    public Cat(){
        super("ネコ");
    }

    @Override
    public void naku(){
        System.out.println("ニャーニャー");
    }
}