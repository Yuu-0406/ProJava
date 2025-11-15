public class Dog extends Animal{
    public Dog(){
        super("イヌ");
    }

    @Override
    public void naku(){
        System.out.println("ワンワン");
    }
}