public class WageCalculator {
    public int wage_person(int hours, int holiday, int HourlyWage){
        int expected = 0;
        if (hours>40){
            expected = hours - 40;
        }
        var salary = (int) (40*(HourlyWage)+(1.5*(expected)*(HourlyWage))+(2*(holiday)*(HourlyWage)));
        return salary;
    }
}
