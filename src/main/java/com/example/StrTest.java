public class StrTest {
    public static void main(String[] args) {
        if(args.length <= 0)
            return;

        String str = args[0];
        String str2 = "xyz";
        System.out.println(str.length());
        System.out.println(str.toUpperCase());
        System.out.println(str.concat(str2));
        System.out.println(str + str2 + str);
        System.out.println(str.charAt(1));
        System.out.println(str.equalsIgnoreCase("Abc"));
    }
}