class Circle{
    private int radius;

    Circle(int radius){
        this.radius = radius;
    }

    int getRadius(){
        return radius;
    }

    //同値判定に用いるメソッド
    @Override
    public boolean equals(Object obj){
        if (obj instanceof Circle){
            Circle other = (Circle) obj;
            return (this.radius == other.radius);
        } else{
            return false;
        }
    }

    //equals メソッドをオーバーライドする場合は
    //必ずこのメソッドもオーバーライドすること
    @Override
    public int hashCode(){
        return radius;
    }
}

public class EqualsTest{
    public static void main(String[] args) {
        Circle circleA = new Circle(5);
        Circle circleB = new Circle(5);

        System.out.println("circleA's radius : " + circleA.getRadius());
        System.out.println("circleB's radius : " + circleB.getRadius());

        System.out.println("circleA == circleB : " + (circleA == circleB));
        System.out.println("circleA.equals(circleB) : " + circleA.equals(circleB));
    }
}