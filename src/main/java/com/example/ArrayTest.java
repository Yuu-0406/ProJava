public class ArrayTest{
    public static void main(String[] args) {
        int[] a;
        int[] b;

        a = new int[10];
        a[0] = 10;
        a[1] = 11;

        b = a;
        b[0] = 20;
        b[1] = 21;

        System.out.println(a[0]);
        System.out.println(a[1]);
        System.out.println(b[0]);
        System.out.println(b[1]);
    }
}