package entity;

public class Country {
    private String code;
    private String name;
    private String region;

    public Country(String code, String name, String region) {
        this.code = code;
        this.name = name;
        this.region = region;
    }

    public Country() {
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    @Override
    public String toString() {
        return code + '\t' + name + '\t'+ region  ;
    }
}
