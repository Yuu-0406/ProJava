public class Concat{
    public static void main(String[] args) {
        //文字列+...
        System.out.println("abc"+"ABC");
        System.out.println("abc"+'A');
        System.out.println("abc"+12);
        System.out.println("abc"+3.45);

        //文字+...
        System.out.println('a'+"ABC");
        System.out.println('a'+'A');
        System.out.println('a'+12);
        System.out.println('a'+3.45);

        //数値+...
        System.out.println(678+"ABC");
        System.out.println(678+'A');
        System.out.println(678+12);
        System.out.println(678+3.45);

        //複合
        System.out.println('a'+10+"ABC");
        System.out.println('a'+(10+"ABC"));

        //変数
        int x = 2;
        int y = 3;
        System.out.println(x + " + " + y + " = " + (x+y));
    }
}