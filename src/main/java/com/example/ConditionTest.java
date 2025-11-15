
public class ConditionTest{
    public static void main(String[] args) {
        int a, b;

        a = 9;
        b = 0;
        if (a == 10 && 10 == (b = 2*5)){
            System.out.println("a == 10, b ==10");
        }
        System.out.println(a);
        System.out.println(b);

        a = 9;
        b = 0;
        if (a == 10 & 10 ==(b - 2*5)){
            System.out.println("a == 10, b ==10");
        }
        System.out.println(a);
        System.out.println(b);
    }
}