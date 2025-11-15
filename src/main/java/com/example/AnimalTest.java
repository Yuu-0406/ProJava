public class AnimalTest{
    public static void nakigoeTest(Animal animal){
        if (animal instanceof Dog){
            System.out.println("お犬様の鳴き声 : ");
        } else if (animal instanceof Cat){
            System.out.println("気まぐれネコさんの鳴き声 : ");
        } else {
            System.out.print("UMAの鳴き声 : ");
        }
        animal.naku();
        
        
    }
    

    public static void main(String[] args) {
        
        Animal pochi = new Dog();
        Animal tama = new Cat();

        nakigoeTest(pochi);
        nakigoeTest(tama);
    }
}