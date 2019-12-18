
from django.db import models
from django.contrib.gis.db.models import PointField, MultiPolygonField

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey('Province', related_name='district',
                                 on_delete=models.CASCADE)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', related_name='municipality',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)
    hlcit_code = models.CharField(max_length=100, blank=True, null=True)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


# class Question(models.Model):
#     question = models.CharField(max_length=2000)
#
#     def __str__(self):
#         return self.question

#
# class QuestionData(models.Model):
#     question = models.ForeignKey('Question', related_name='question', on_delete=models.CASCADE)
#     house_hold = models.ForeignKey('HouseHold', related_name='question',
#                                    on_delete=models.CASCADE)


# class Responder(models.Model):
#     name = models.CharField(max_length=200)
#     gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
#     age = models.CharField(max_length=5)
#     contact = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name


# class DamageType(models.Model):
#     DAMAGES_TYPE = (
#         (1, 'Death/Injured family members'),
#         (2, 'House'),
#         (3, 'Furniture'),
#         (4, 'Land'),
#         (5, 'Livestock'),
#         (6, 'Machinery'),
#         (7, 'Crops'),
#         (8, 'Personal documents'),
#         (9, 'Food Stock'),
#         (10, 'None'),
#         (12, 'Others'),
#     )
#     damages = models.BooleanField()
#     damage_type = models.IntegerField(choices=DAMAGES_TYPE, default=1)
#     damage_other = models.CharField(max_length=500, blank=True, null=True)
#
#
# class DisasterProne(models.Model):
#     DISASTER_CHOICES = (
#         (1, 'Flood prone area'),
#         (2, 'Landslide prone area'),
#         (3, 'Fire prone area'),
#         (4, 'Black Spot'),
#         (5, 'Animal attack'),
#         (6, 'Lightening'),
#         (7, 'Road accident'),
#         (8, 'Cold wind'),
#         (9, 'Earthquake'),
#         (10, 'Thunderstorm'),
#         (11, 'Flood'),
#         (12, 'Windstorm'),
#         (13, 'Epidemic'),
#         (14, 'Others')
#     )
#     name = models.IntegerField(choices=DISASTER_CHOICES, default=1)
#     disaster_other = models.CharField(max_length=500, blank=True, null=True)
#     damage_type = models.ForeignKey('DamageType', on_delete=models.CASCADE, blank=True, null=True)
#     migration = models.BooleanField()
#     place = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class VulnerablePopulation(models.Model):
#     POPULATION_CHOICES = (
#         (1, 'Pregnant'),
#         (2, 'Breast feeding woman'),
#         (3, 'Single Woman/widow'),
#         (4, 'Senior Citizen'),
#         (5, 'People with disability'),
#         (6, 'Chronic illness'),
#         (7, 'Nutrition support'),
#     )
#     name = models.IntegerField(choices=POPULATION_CHOICES, default=1)

# class Occupation(models.Model):
#
#     OCCUPATION_CHOICES = (
#         (1, 'Agriculture'),
#         (2, 'Agricultural wages'),
#         (3, 'Daily wages'),
#         (4, 'Government service'),
#         (5, 'Non-government service'),
#         (6, 'Foreign employment'),
#         (7, 'Entrepreneur'),
#         (8, 'Business'),
#         (9, 'Seasonal labor, India'),
#         (10, 'Seasonal labor, Nepal'),
#         (11, 'Student'),
#         (12, 'Other'),
#
#     )
#     BUSINESS_TYPE = (
#         (1, 'shop'),
#         (1, 'Pharmacy'),
#         (1, 'Stationery'),
#         (1, 'Hardware shop'),
#         (1, 'Hotel/Restaurant'),
#         (1, 'Poultry farming'),
#         (1, 'Livestock farming'),
#         (1, 'Cattle farming'),
#         (1, 'Other agricultural business'),
#         (1, 'Other small business'),
#         (1, 'Other'),
#     )
#
#     occupation = models.IntegerField(choices=OCCUPATION_CHOICES, default=1)
#     data = models.BooleanField(default=False)
#     if_other_occupation = models.CharField(max_length=300, blank=True, null=True)
#     if_other_business_occupation = models.CharField(max_length=300, blank=True, null=True)
#     if_other_agriculture_business = models.CharField(max_length=300, blank=True, null=True)
#     if_other_small_business = models.CharField(max_length=300, blank=True, null=True)
#
#     def __str__(self):
#         return self.occupation
#
#
# class HouseHold(models.Model):
#     GENDER_CHOICES = (
#         (1, 'Male'),
#         (2, 'Female')
#     )
#
#     OWNERSHIP_CHOICES = (
#         (1, 'Male leadership'),
#         (2, 'Female’s leadership'),
#         (3, 'Senior Citizen’s leadership'),
#         (4, 'Children’s leadership'),
#         (5, 'Single woman’s leadership'),
#         (6, 'Disabled member’s leadership'),
#         (7, 'other'),
#     )
#     ETHNICITY = (
#         (1, 'Brahmin'),
#         (2, 'Chhetri'),
#         (3, 'Terai Janajati'),
#         (4, 'Pahadi Janajati'),
#         (5, 'Terai Dalit'),
#         (6, 'Pahadi Dalit'),
#         (7, 'Muslim'),
#         (8, 'Newar'),
#         (9, 'Other'),
#     )
#     RELIGION_CHOICE = (
#         (1, 'Hindu'),
#         (2, 'Karmiya Baidya'),
#         (3, 'Mushlim'),
#         (4, 'others')
#     )
#
#     MOTHER_TONGUE_CHOICE = (
#         (1, 'Nepali'),
#         (1, 'Maithili'),
#         (1, 'Bhojpuri'),
#         (1, 'Newari'),
#         (1, 'Tamang'),
#         (1, 'Gurung'),
#         (1, 'Limbu'),
#         (1, 'Tharu'),
#         (1, 'Rajbansi'),
#         (1, 'Awadi'),
#         (1, 'Kirati'),
#         (1, 'Other'),
#     )
#     EDUCATION_CHOICES = (
#         (1, 'Illiterate'),
#         (2, 'Literate'),
#         (3, 'Primary level (1-8)'),
#         (4, 'Secondary level (9-12)'),
#         (5, 'Bachelor degree'),
#         (6, 'Master’s degree'),
#         (7, 'P.hd'),
#     )
#
#     start_date = models.DateTimeField(blank=True, null=True)
#     end_date = models.DateTimeField(blank=True, null=True)
#     surveyor_name = models.CharField(max_length=500)
#     name_of_place = models.CharField(max_length=500)
#     ward_no = models.IntegerField(blank=True, null=True)
#     location = models.PointField(geography=True, srid=4326, blank=True, null=True)
#     altitude = models.CharField(max_length=100, blank=True, null=True)
#     precision = models.CharField(max_length=100, blank=True, null=True)
#     household_no = models.IntegerField(blank=True, null=True)
#     house_holder_name = models.CharField(max_length=500, blank=True, null=True)
#     age_of_owner = models.IntegerField()
#     gender_of_house_owner = models.IntegerField(choices=GENDER_CHOICES, default=1)
#     status_of_owner = models.IntegerField(choices=OWNERSHIP_CHOICES, default=1)
#     if_other_owner_status = models.CharField(max_length=500, blank=True, null=True)
#     ethnicity = models.IntegerField(choices=ETHNICITY, default=1)
#     other_ethnicity = models.CharField(max_length=200, blank=True, null=True)
#     religion = models.IntegerField(choices=RELIGION_CHOICE, default=1)
#     religion_other = models.CharField(max_length=200, blank=True, null=True)
#     mother_tongue = models.IntegerField(default=1, choices=MOTHER_TONGUE_CHOICE)
#     other_mother_tongue = models.CharField(max_length=200, blank=True, null=True)
#     contact_num = models.CharField(max_length=50, blank=True, null=True)
#     education_level = models.IntegerField(choices=EDUCATION_CHOICES, default=1)
#     owner_citizenship_number = models.CharField(max_length=100, blank=True, null=True)
#     responder_name = models.CharField(max_length=200, blank=True, null=True)
#     responder_gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
#     responder_age = models.CharField(max_length=5, blank=True, null=True)
#     responder_contact = models.CharField(max_length=20, blank=True, null=True)
#     other_family_member = models.BooleanField(default=False)
#     occupation = models.ForeignKey('Occupation', on_delete=models.CASCADE, related_name= 'house_hold')
#
#
#
#     @property
#     def latitude(self):
#         return self.location.y
#
#     @property
#     def longitude(self):
#         return self.location.x
#
#     def __str__(self):
#         return self.house_holder_name + ',' + self.name_of_place
#
#
# class FamilyMembersCriteria(models.Model):
#     CHOICES = (
#         (1, 'Senior citizen of 70 years'),
#         (1, 'Senior Citizen of 60 years'),
#         (1, 'Unmarried 60 years old woman'),
#         (1, '60 years old single woman'),
#         (1, 'Widow of any age'),
#         (1, 'People with disability of any age'),
#         (1, 'Widow of any age'),
#     )
#
#
# class OwnerFamily(models.Model):
#     GENDER_CHOICES = (
#         (1, 'Male'),
#         (2, 'Female')
#     )
#     INVOLVEMENT_IN_OCCUPATION = (
#         (1, 'Active'),
#         (2, 'Inactive')
#     )
#     FAMILY_MEMBER_CRITERIA = (
#         (1, 'Senior citizen of 70 years'),
#         (2, ''),
#         (1, 'Senior citizen of 70 years'),
#         (1, 'Senior citizen of 70 years'),
#         (1, 'Senior citizen of 70 years'),
#         (1, 'Senior citizen of 70 years'),
#     )
#
#     name = models.CharField(max_length=200)
#     age_group = models.IntegerField()
#     education_level = models.IntegerField()
#     gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
#     occupation_of_family = models.CharField(max_length=500, blank=True, null=True)
#     involvement_in_occupation = models.IntegerField(choices=INVOLVEMENT_IN_OCCUPATION, default=1)
#     monthly_income = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
#     household = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='owner_family')
#     # does_family_member meet_any_of_the_criteria = models.IntegerField()
#
#     def __str__(self):
#         return self.name
#
#
# class AnimalDetail(models.Model):
#     type_of_livestock = models.CharField(max_length=100)
#     number_of_livestock = models.IntegerField()
#     commercial_purpose = models.BooleanField(default=False)
#     household = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='owner_family')
#
#     def __str__(self):
#         return self.type_of_livestock


class Survey(models.Model):
    S_CHOICES = (
        (1, 'Male'),
        (2, 'Female')
    )
    t_choices = (
        (1, 'Male leadership'),
        (1, 'Female’s leadership'),
        (1, 'Disabled member’s leadership'),
        (1, 'Children’s leadership'),
        (1, 'Single woman’s leadership'),
        (1, 'other'),
    )

    a = models.IntegerField()
    b = models.DateTimeField(blank=True, null=True)
    c = models.DateTimeField(blank=True, null=True)
    d = models.DateField(blank=True, null=True)
    e = models.CharField(max_length=40, blank=True, null=True)
    f = models.DateField(blank=True, null=True)
    g = models.CharField(max_length=500)
    h = models.CharField(max_length=500)
    i = models.IntegerField(blank=True, null=True)
    j = models.IntegerField(blank=True, null=True)
    l = models.CharField(max_length=50)
    m = models.CharField(max_length=50)
    n = models.CharField(max_length=50)
    o = models.CharField(max_length=50)
    p = models.IntegerField(blank=True, null=True)
    q = models.CharField(max_length=500, blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    s = models.CharField(max_length=500, blank=True, null=True)
    t = models.CharField(max_length=500, blank=True, null=True)
    u = models.CharField(max_length=500, blank=True, null=True)
    v = models.CharField(max_length=500, blank=True, null=True)
    w = models.CharField(max_length=500, blank=True, null=True)
    x = models.CharField(max_length=500, blank=True, null=True)
    y = models.CharField(max_length=500, blank=True, null=True)
    z = models.CharField(max_length=500, blank=True, null=True)
    aa = models.CharField(max_length=500, blank=True, null=True)
    ab = models.CharField(max_length=500, blank=True, null=True)
    ac = models.CharField(max_length=500, blank=True, null=True)
    ad = models.CharField(max_length=500, blank=True, null=True)
    ae = models.CharField(max_length=500, blank=True, null=True)
    af = models.CharField(max_length=500, blank=True, null=True)
    ag = models.IntegerField()
    ah = models.CharField(max_length=100, blank=True, null=True)
    ai = models.BooleanField(default=False)
    aj = models.CharField(max_length=400, blank=True, null=True)
    ak = models.BooleanField()
    al = models.BooleanField()
    am = models.BooleanField()
    an = models.BooleanField()
    ao = models.BooleanField()
    ap = models.BooleanField()
    aq = models.BooleanField()
    ar = models.BooleanField()
    as_a = models.BooleanField()
    at = models.BooleanField()
    au = models.BooleanField()
    av = models.CharField(max_length=100, blank=True, null=True)
    aw = models.CharField(max_length=100, blank=True, null=True)
    ax = models.CharField(max_length=100, blank=True, null=True)
    ay = models.CharField(max_length=100, blank=True, null=True)
    az = models.CharField(max_length=100, blank=True, null=True)
    ba = models.CharField(max_length=100, blank=True, null=True)
    bb = models.CharField(max_length=100, blank=True, null=True)
    bc = models.CharField(max_length=100, blank=True, null=True)
    bd = models.CharField(max_length=100, blank=True, null=True)
    be = models.CharField(max_length=100, blank=True, null=True)
    bf = models.CharField(max_length=100, blank=True, null=True)
    bg = models.CharField(max_length=100, blank=True, null=True)
    bh = models.CharField(max_length=100, blank=True, null=True)
    bi = models.CharField(max_length=100, blank=True, null=True)
    bj = models.CharField(max_length=100, blank=True, null=True)
    bk = models.CharField(max_length=100, blank=True, null=True)
    bl = models.CharField(max_length=100, blank=True, null=True)
    bm = models.CharField(max_length=100, blank=True, null=True)
    bn = models.CharField(max_length=100, blank=True, null=True)
    bo = models.CharField(max_length=100, blank=True, null=True)
    bp = models.CharField(max_length=100, blank=True, null=True)
    bq = models.CharField(max_length=100, blank=True, null=True)
    br = models.CharField(max_length=100, blank=True, null=True)
    bs = models.CharField(max_length=100, blank=True, null=True)
    bt = models.CharField(max_length=100, blank=True, null=True)
    bu = models.CharField(max_length=100, blank=True, null=True)
    bv = models.CharField(max_length=100, blank=True, null=True)
    bw = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    bx = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    by = models.BooleanField()
    bz = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    ca = models.CharField(max_length=100, blank=True, null=True)
    cb = models.BooleanField()
    cc = models.BooleanField()
    cd = models.CharField(max_length=1000, blank=True, null=True)
    ce = models.BooleanField(default=False)
    cf = models.BooleanField(default=False)
    cg = models.BooleanField(default=False)
    ch = models.BooleanField(default=False)
    ci = models.BooleanField(default=False)
    cj = models.CharField(max_length=1000, blank=True, null=True)
    ck = models.CharField(max_length=1000, blank=True, null=True)
    cl = models.BooleanField(default=False)
    cm = models.BooleanField(default=False)
    cn = models.BooleanField(default=False)
    co = models.BooleanField(default=False)
    cp = models.BooleanField(default=False)
    cq = models.BooleanField(default=False)
    cr = models.BooleanField(default=False)
    cs = models.BooleanField(default=False)
    ct = models.BooleanField(default=False)
    cu = models.CharField(max_length=1000, blank=True, null=True)
    cv = models.CharField(max_length=1000, blank=True, null=True)
    cw = models.BooleanField(default=False)
    cx = models.BooleanField(default=False)
    cy = models.BooleanField(default=False)
    cz = models.BooleanField(default=False)
    da = models.BooleanField(default=False)
    db = models.BooleanField(default=False)
    dc = models.BooleanField(default=False)
    dd = models.BooleanField(default=False)
    de = models.BooleanField(default=False)
    df = models.CharField(max_length=1000, blank=True, null=True)
    dg = models.BooleanField(default=False)
    dh = models.BooleanField(default=False)
    di = models.BooleanField(default=False)
    dj = models.BooleanField(default=False)
    dk = models.BooleanField(default=False)
    dl = models.BooleanField(default=False)
    dm = models.BooleanField(default=False)
    dn = models.BooleanField(default=False)
    do = models.CharField(max_length=1000, blank=True, null=True)
    dp = models.CharField(max_length=100, blank=True, null=True)
    dq = models.BooleanField(default=False)
    dr = models.BooleanField(default=False)
    ds = models.BooleanField(default=False)
    dt = models.CharField(max_length=1000, blank=True, null=True)
    du = models.BooleanField(default=False)
    dv = models.BooleanField(default=False)
    dw = models.BooleanField(default=False)
    dx = models.BooleanField(default=False)
    dy = models.BooleanField(default=False)
    dz = models.BooleanField(default=False)
    ea = models.BooleanField(default=False)
    eb = models.CharField(max_length=1000, blank=True, null=True)
    ec = models.CharField(max_length=10, blank=True, null=True)
    ed = models.CharField(max_length=10, blank=True, null=True)
    ee = models.IntegerField(blank=True, null=True)
    ef = models.CharField(max_length=10, blank=True, null=True)
    eg = models.BooleanField(default=False)
    eh = models.BooleanField(default=False)
    ei = models.BooleanField(default=False)
    ej = models.BooleanField(default=False)
    ek = models.CharField(max_length=100, blank=True, null=True)
    el = models.BooleanField(default=False)
    em = models.BooleanField(default=False)
    en = models.BooleanField(default=False)
    eo = models.CharField(max_length=100, blank=True, null=True)
    ep = models.CharField(max_length=1000, blank=True, null=True)
    eq = models.CharField(max_length=1000, blank=True, null=True)
    er = models.BooleanField(default=False)
    es = models.CharField(max_length=1000, blank=True, null=True)
    et = models.ImageField(blank=True, null=True)
    eu = models.BooleanField(default=False)
    ev = models.CharField(max_length=1000, blank=True, null=True)
    ew = models.BooleanField(default=False)
    ex = models.BooleanField(default=False)
    ey = models.BooleanField(default=False)
    ez = models.BooleanField(default=False)
    fa = models.BooleanField(default=False)
    fb = models.BooleanField(default=False)
    fc = models.BooleanField(default=False)
    fd = models.BooleanField(default=False)
    fe = models.BooleanField(default=False)
    ff = models.BooleanField(default=False)
    fg = models.BooleanField(default=False)
    fh = models.BooleanField(default=False)
    fi = models.BooleanField(default=False)
    fj = models.BooleanField(default=False)
    fk = models.BooleanField(default=False)
    fl = models.IntegerField(blank=True, null=True)
    fm = models.IntegerField(blank=True, null=True)
    fn = models.IntegerField(blank=True, null=True)
    fo = models.BooleanField(default=False)
    fp = models.BooleanField(default=False)
    fq = models.BooleanField(default=False)
    fr = models.IntegerField(blank=True, null=True)
    fs = models.IntegerField(blank=True, null=True)
    ft = models.BooleanField(default=False)
    fu = models.BooleanField(default=False)
    fv = models.BooleanField(default=False)
    fw = models.IntegerField(blank=True, null=True)
    fx = models.IntegerField(blank=True, null=True)
    fy = models.BooleanField(default=False)
    fz = models.BooleanField(default=False)
    ga = models.BooleanField(default=False)
    gb = models.IntegerField(blank=True, null=True)
    gc = models.IntegerField(blank=True, null=True)
    gd = models.BooleanField(default=False)
    ge = models.BooleanField(default=False)
    gf = models.BooleanField(default=False)
    gg = models.IntegerField(blank=True, null=True)
    gh = models.IntegerField(blank=True, null=True)
    gi = models.BooleanField(default=False)
    gj = models.BooleanField(default=False)
    gk = models.BooleanField(default=False)
    gl = models.IntegerField(blank=True, null=True)
    gm = models.IntegerField(blank=True, null=True)
    gn = models.BooleanField(default=False)
    go = models.BooleanField(default=False)
    gp = models.BooleanField(default=False)
    gq = models.IntegerField(blank=True, null=True)
    gr = models.IntegerField(blank=True, null=True)
    gs = models.BooleanField(default=False)
    gt = models.BooleanField(default=False)
    gu = models.BooleanField(default=False)
    gv = models.IntegerField(blank=True, null=True)
    gw = models.IntegerField(blank=True, null=True)
    gx = models.BooleanField(default=False)
    gy = models.BooleanField(default=False)
    gz = models.BooleanField(default=False)
    ha = models.IntegerField(blank=True, null=True)
    hb = models.IntegerField(blank=True, null=True)
    hc = models.BooleanField(default=False)
    hd = models.BooleanField(default=False)
    he = models.BooleanField(default=False)
    hf = models.IntegerField(blank=True, null=True)
    hg = models.IntegerField(blank=True, null=True)
    hh = models.CharField(max_length=500)
    hi = models.CharField(max_length=100, blank=True, null=True)
    hj = models.IntegerField(blank=True, null=True)
    hk = models.IntegerField(blank=True, null=True)
    hl = models.CharField(max_length=500, blank=True, null=True)
    hm = models.CharField(max_length=500, blank=True, null=True)
    hn = models.IntegerField(blank=True, null=True)
    ho = models.CharField(max_length=500, blank=True, null=True)
    hp = models.CharField(max_length=500, blank=True, null=True)
    hq = models.CharField(max_length=500, blank=True, null=True)
    hr = models.CharField(max_length=500, blank=True, null=True)
    hs = models.CharField(max_length=500, blank=True, null=True)
    ht = models.CharField(max_length=500, blank=True, null=True)
    hu = models.CharField(max_length=500, blank=True, null=True)
    hv = models.CharField(max_length=500, blank=True, null=True)
    hw = models.CharField(max_length=500, blank=True, null=True)
    hx = models.CharField(max_length=500, blank=True, null=True)
    hy = models.CharField(max_length=500, blank=True, null=True)
    hz = models.BooleanField(default=False)
    ia = models.BooleanField(default=False)
    ib = models.BooleanField(default=False)
    ic = models.BooleanField(default=False)
    id_i = models.BooleanField(default=False)
    ie = models.BooleanField(default=False)
    if_i = models.BooleanField(default=False)
    ig = models.CharField(max_length=500, blank=True, null=True)
    ih = models.CharField(max_length=500, blank=True, null=True)
    ii = models.CharField(max_length=500, blank=True, null=True)
    ij = models.IntegerField(blank=True, null=True)
    ik = models.CharField(max_length=500, blank=True, null=True)
    il = models.CharField(max_length=500, blank=True, null=True)
    im = models.CharField(max_length=500, blank=True, null=True)
    in_i = models.BooleanField(default=False)
    io = models.BooleanField(default=False)
    ip = models.BooleanField(default=False)
    iq = models.BooleanField(default=False)
    ir = models.BooleanField(default=False)
    is_i = models.BooleanField(default=False)
    it = models.BooleanField(default=False)
    iu = models.CharField(max_length=500, blank=True, null=True)
    iv = models.CharField(max_length=500, blank=True, null=True)
    iw = models.CharField(max_length=500, blank=True, null=True)
    ix = models.BooleanField(default=False)
    iy = models.BooleanField(default=False)
    iz = models.BooleanField(default=False)
    ja = models.BooleanField(default=False)
    jb = models.BooleanField(default=False)
    jc = models.BooleanField(default=False)
    jd = models.BooleanField(default=False)
    je = models.BooleanField(default=False)
    jf = models.BooleanField(default=False)
    jg = models.BooleanField(default=False)
    jh = models.BooleanField(default=False)
    ji = models.BooleanField(default=False)
    jj = models.CharField(max_length=500, blank=True, null=True)
    jk = models.CharField(max_length=500, blank=True, null=True)
    jl = models.BooleanField(default=False)
    jm = models.BooleanField(default=False)
    jn = models.BooleanField(default=False)
    jo = models.BooleanField(default=False)
    jp = models.BooleanField(default=False)
    jq = models.BooleanField(default=False)
    jr = models.BooleanField(default=False)
    js = models.BooleanField(default=False)
    jt = models.BooleanField(default=False)
    ju = models.BooleanField(default=False)
    jv = models.BooleanField(default=False)
    jw = models.BooleanField(default=False)
    jx = models.CharField(max_length=500, blank=True, null=True)
    jy = models.CharField(max_length=500, blank=True, null=True)
    jz = models.CharField(max_length=500, blank=True, null=True)
    ka = models.BooleanField(default=False)
    kb = models.BooleanField(default=False)
    kc = models.BooleanField(default=False)
    kd = models.BooleanField(default=False)
    ke = models.BooleanField(default=False)
    kf = models.BooleanField(default=False)
    kg = models.BooleanField(default=False)
    kh = models.CharField(max_length=500, blank=True, null=True)
    ki = models.BooleanField(default=False)
    kj = models.BooleanField(default=False)
    kk = models.BooleanField(default=False)
    kl = models.CharField(max_length=500, blank=True, null=True)
    km = models.CharField(max_length=500, blank=True, null=True)
    kn = models.BooleanField(default=False)
    ko = models.BooleanField(default=False)
    kp = models.BooleanField(default=False)
    kq = models.BooleanField(default=False)
    kr = models.BooleanField(default=False)
    ks = models.BooleanField(default=False)
    kt = models.CharField(max_length=500, blank=True, null=True)
    ku = models.CharField(max_length=500, blank=True, null=True)
    kv = models.CharField(max_length=500, blank=True, null=True)
    kw = models.IntegerField(blank=True, null=True)
    kx = models.CharField(max_length=500, blank=True, null=True)
    ky = models.CharField(max_length=500, blank=True, null=True)
    kz = models.CharField(max_length=500, blank=True, null=True)
    la = models.BooleanField(default=False)
    lb = models.BooleanField(default=False)
    lc = models.BooleanField(default=False)
    ld = models.BooleanField(default=False)
    le = models.BooleanField(default=False)
    lf = models.BooleanField(default=False)
    lg = models.BooleanField(default=False)
    lh = models.BooleanField(default=False)
    li = models.BooleanField(default=False)
    lj = models.BooleanField(default=False)
    lk = models.BooleanField(default=False)
    ll = models.BooleanField(default=False)
    lm = models.CharField(max_length=500, blank=True, null=True)
    ln = models.CharField(max_length=500, blank=True, null=True)
    lo = models.CharField(max_length=500, blank=True, null=True)
    lp = models.BooleanField(default=False)
    lq = models.BooleanField(default=False)
    lr = models.CharField(max_length=500, blank=True, null=True)
    ls = models.BooleanField(default=False)
    lt = models.CharField(max_length=1000, blank=True, null=True)
    lu = models.BooleanField(default=False)
    lv = models.BooleanField(default=False)
    lw = models.BooleanField(default=False)
    lx = models.BooleanField(default=False)
    ly = models.BooleanField(default=False)
    lz = models.BooleanField(default=False)
    ma = models.BooleanField(default=False)
    mb = models.BooleanField(default=False)
    mc = models.BooleanField(default=False)
    md = models.BooleanField(default=False)
    me = models.CharField(max_length=500, blank=True, null=True)
    mf = models.BooleanField(default=False)
    mg = models.CharField(max_length=500, blank=True, null=True)
    mh = models.BooleanField(default=False)
    mi = models.CharField(max_length=500, blank=True, null=True)
    mj = models.BooleanField(default=False)
    mk = models.BooleanField(default=False)
    ml = models.BooleanField(default=False)
    mm = models.BooleanField(default=False)
    mn = models.BooleanField(default=False)
    mo = models.BooleanField(default=False)
    mp = models.BooleanField(default=False)
    mq = models.BooleanField(default=False)
    mr = models.CharField(max_length=500, blank=True, null=True)
    ms = models.BooleanField(default=False)
    mt = models.CharField(max_length=500, blank=True, null=True)
    mu = models.BooleanField(default=False)
    mv = models.BooleanField(default=False)
    mw = models.BooleanField(default=False)
    mx = models.BooleanField(default=False)
    my = models.BooleanField(default=False)
    mz = models.CharField(max_length=500, blank=True, null=True)
    na = models.BooleanField(default=False)
    nb = models.BooleanField(default=False)
    nc = models.BooleanField(default=False)
    nd = models.BooleanField(default=False)
    ne = models.BooleanField(default=False)
    nf = models.CharField(max_length=500, blank=True, null=True)
    ng = models.BooleanField(default=False)
    nh = models.BooleanField(default=False)
    ni = models.BooleanField(default=False)
    nj = models.BooleanField(default=False)
    nk = models.CharField(max_length=500, blank=True, null=True)
    nl = models.BooleanField(default=False)
    nm = models.CharField(max_length=500, blank=True, null=True)
    nn = models.CharField(max_length=500, blank=True, null=True)
    no = models.CharField(max_length=500, blank=True, null=True)
    np = models.BooleanField(default=False)
    nq = models.BooleanField(default=False)
    nr = models.BooleanField(default=False)
    ns = models.BooleanField(default=False)
    nt = models.BooleanField(default=False)
    nu = models.BooleanField(default=False)
    nv = models.BooleanField(default=False)
    nw = models.BooleanField(default=False)
    nx = models.BooleanField(default=False)
    ny = models.BooleanField(default=False)
    nz = models.CharField(max_length=500, blank=True, null=True)
    oa = models.CharField(max_length=500, blank=True, null=True)
    ob = models.BooleanField(default=False)
    oc = models.BooleanField(default=False)
    od = models.BooleanField(default=False)
    oe = models.BooleanField(default=False)
    of = models.BooleanField(default=False)
    og = models.BooleanField(default=False)
    oh = models.BooleanField(default=False)
    oi = models.CharField(max_length=500, blank=True, null=True)
    oj = models.CharField(max_length=500, blank=True, null=True)
    ok = models.CharField(max_length=500, blank=True, null=True)
    ol = models.CharField(max_length=500, blank=True, null=True)
    om = models.BooleanField(default=False)
    on = models.BooleanField(default=False)
    oo = models.BooleanField(default=False)
    op = models.BooleanField(default=False)
    oq = models.BooleanField(default=False)
    or_o = models.BooleanField(default=False)
    os = models.BooleanField(default=False)
    ot = models.CharField(max_length=500, blank=True, null=True)
    ou = models.CharField(max_length=500, blank=True, null=True)
    ov = models.BooleanField(default=False)
    ow = models.BooleanField(default=False)
    ox = models.BooleanField(default=False)
    oy = models.BooleanField(default=False)
    oz = models.BooleanField(default=False)
    pa = models.CharField(max_length=500, blank=True, null=True)
    pb = models.BooleanField(default=False)
    pc = models.CharField(max_length=500, blank=True, null=True)
    pd = models.CharField(max_length=500, blank=True, null=True)
    pe = models.BooleanField(default=False)
    pf = models.BooleanField(default=False)
    pg = models.BooleanField(default=False)
    ph = models.BooleanField(default=False)
    pi = models.BooleanField(default=False)
    pj = models.BooleanField(default=False)
    pk_p = models.BooleanField(default=False)
    pl = models.CharField(max_length=500, blank=True, null=True)
    pm = models.CharField(max_length=500, blank=True, null=True)
    pn = models.BooleanField(default=False)
    po = models.BooleanField(default=False)
    pp = models.BooleanField(default=False)
    pq = models.BooleanField(default=False)
    pr = models.BooleanField(default=False)
    ps = models.CharField(max_length=500, blank=True, null=True)
    pt = models.BooleanField(default=False)
    pu = models.CharField(max_length=500, blank=True, null=True)
    pv = models.BooleanField(default=False)
    pw = models.BooleanField(default=False)
    px = models.BooleanField(default=False)
    py = models.BooleanField(default=False)
    pz = models.BooleanField(default=False)
    qa = models.CharField(max_length=500, blank=True, null=True)
    qb = models.CharField(max_length=500, blank=True, null=True)
    qc = models.BooleanField(default=False)
    qd = models.BooleanField(default=False)
    qe = models.BooleanField(default=False)
    qf = models.BooleanField(default=False)
    qg = models.BooleanField(default=False)
    qh = models.BooleanField(default=False)
    qi = models.BooleanField(default=False)
    qj = models.CharField(max_length=500, blank=True, null=True)
    qk = models.CharField(max_length=500, blank=True, null=True)
    ql = models.CharField(max_length=500, blank=True, null=True)
    qm = models.BooleanField(default=False)
    qn = models.BooleanField(default=False)
    qo = models.CharField(max_length=500, blank=True, null=True)
    qp = models.CharField(max_length=500, blank=True, null=True)
    qq = models.CharField(max_length=500, blank=True, null=True)
    qr = models.CharField(max_length=500, blank=True, null=True)
    qs = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.q


class FamilyMembers(models.Model):
    a = models.CharField(max_length=200, blank=True, null=True)
    b = models.CharField(max_length=200, blank=True, null=True)
    c = models.CharField(max_length=200, blank=True, null=True)
    d = models.CharField(max_length=200, blank=True, null=True)
    e = models.CharField(max_length=200, blank=True, null=True)
    f = models.CharField(max_length=200, blank=True, null=True)
    g = models.CharField(max_length=200, blank=True, null=True)
    h = models.BooleanField(default=False)
    i = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    j = models.CharField(max_length=200, blank=True, null=True)
    k = models.BooleanField(default=False)
    l = models.BooleanField(default=False)
    m = models.BooleanField(default=False)
    n = models.BooleanField(default=False)
    o = models.BooleanField(default=False)
    p = models.BooleanField(default=False)
    q = models.BooleanField(default=False)
    r = models.BooleanField(default=False)
    s = models.BooleanField(default=False)
    t = models.BooleanField(default=False)
    u = models.CharField(max_length=200, blank=True, null=True)
    w = models.CharField(max_length=1000, blank=True, null=True)
    x = models.CharField(max_length=1000, blank=True, null=True)
    y = models.BooleanField(default=False)
    z = models.BooleanField(default=False)
    aa = models.BooleanField(default=False)
    ab = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    ad = models.BooleanField(default=False)
    ae = models.BooleanField(default=False)
    af = models.BooleanField(default=False)
    ag = models.BooleanField(default=False)
    ah = models.CharField(max_length=1000, blank=True, null=True)
    ai = models.CharField(max_length=1000, blank=True, null=True)
    aj = models.BooleanField(default=False)
    ak = models.BooleanField(default=False)
    al = models.BooleanField(default=False)
    am = models.BooleanField(default=False)
    an = models.BooleanField(default=False)
    ao = models.BooleanField(default=False)
    ap = models.BooleanField(default=False)
    aq = models.BooleanField(default=False)
    ar = models.BooleanField(default=False)
    as_a = models.BooleanField(default=False)
    at = models.BooleanField(default=False)
    au = models.CharField(max_length=1000, blank=True, null=True)
    av = models.CharField(max_length=1000, blank=True, null=True)
    aw = models.BooleanField(default=False)
    ax = models.BooleanField(default=False)
    ay = models.BooleanField(default=False)
    az = models.BooleanField(default=False)
    ba = models.BooleanField(default=False)
    bb = models.BooleanField(default=False)
    bc = models.BooleanField(default=False)
    bd = models.BooleanField(default=False)
    be = models.BooleanField(default=False)
    bf = models.CharField(max_length=1000, blank=True, null=True)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='family_members')

    def __str__(self):
        return self.a


class AnimalDetail(models.Model):
    a = models.CharField(max_length=100)
    b = models.IntegerField()
    c = models.BooleanField(default=False)
    d = models.IntegerField(blank=True, null=True)
    e = models.CharField(blank=True, null=True, max_length=500)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='animal_detail')
    g = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.a



















































































































