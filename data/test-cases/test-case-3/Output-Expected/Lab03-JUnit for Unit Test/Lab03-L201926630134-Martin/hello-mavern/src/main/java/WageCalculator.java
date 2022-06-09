public class WageCalculator {
    private double hourlyWage;
    public double CalculateWage(int standardHours, int holidayHours){
        if(standardHours <= 40){
            if(holidayHours == 0) {
                return standardHours * hourlyWage;
            }
            return holidayHours*hourlyWage*2;
        }
        else{
            if(holidayHours == 0){
                return 40*hourlyWage + (standardHours-40)*1.5;
            }
            return 40*hourlyWage + holidayHours*hourlyWage*2 + (standardHours-40)*1.5;
            }
    }
}
