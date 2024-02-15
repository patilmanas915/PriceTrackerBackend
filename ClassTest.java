class A{
    A(){
        System.out.println("Deafualt Constructor");
    }
    A(int a){
        System.out.println("Parameterized Constructor");
    }
    A(A a){
        System.out.println("Copy Constructor");
    }
}
class ClassTest{
    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new A(10);
        A a3 = new A(a1);
    }
}