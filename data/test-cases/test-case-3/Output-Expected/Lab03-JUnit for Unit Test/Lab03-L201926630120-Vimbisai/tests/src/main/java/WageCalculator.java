public class WageCalculator {

    public double calculateWage(int standard_hours, int holiday_hours, int hourly_wage) {
        double wage;
        if (standard_hours>40){
            wage = (hourly_wage*40)+((standard_hours-40)*1.5*hourly_wage);
        }
        else {
            wage = (hourly_wage * standard_hours);
        }
        wage += (holiday_hours*hourly_wage*2);
        return wage;
    }
}
