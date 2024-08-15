# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math, collections
import pandas as pd



class Renk(models.Model):
    _name = "yaman.renk"
    _description = 'Kapı Rengi'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Renk', required=True, translate=True)


class plastikpervaz(models.Model):
    _name = "yaman.plastik"
    _description = 'PLastik Pervaz'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='PLastik Pervaz tipi ', required=True, translate=True)

class Oda(models.Model):
    _name = "yaman.oda"
    _description = 'Oda'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Oda', required=True, translate=True)


class Project(models.Model):
    _inherit = 'project.project'
    _description = 'yaman.yaman'


    olcu_alan = fields.Many2one('res.users', string='Ölçüyü Alan', index=True)
    kaydi_giren = fields.Many2one('res.users', string="Kaydı Giren", index=True)
    kapi_model = fields.Char(string="Kapı MOdeli")
    yuzey_tipi = fields.Selection([
        ('1', 'PVC'),
        ('2', 'LAKE'),
        ('3', 'MELAMİN'),
        ('4', 'LAMİNANT'),
    ], default='1', index=True, string="Yüzey Tipi", tracking=True)

    seren_tipi = fields.Selection([
        ('1', 'AĞAÇ'),
        ('2', 'MDF'),
    ], default='1', index=True, string="Seren Tipi", tracking=True)
    kasa_rengi = fields.Many2one('yaman.renk', string="Kasa Rengi ")
    yuzey_rengi = fields.Many2one('yaman.renk', string="Yüzey Rengi ")
    pervaz_rengi = fields.Many2one('yaman.renk',string="Pervaz Rengi ")
    yuzey_kalinlik = fields.Integer(string="Yüzey Kalınlığı ")
    kasa_tipi = fields.Selection([
        ('1', 'DÜZ'),
        ('2', 'BOMBE'),
    ], default='1', index=True,string="Kasa tipi" , tracking=True)
    pit_kalinlik = fields.Integer(string="Pervaz İç Taraf Kalınlık")
    pdt_kalinlik = fields.Integer(string="Pervaz Dış Taraf Kalınlık")
    pb_kalinlik = fields.Integer(string="Pervaz Başlık Kalınlık")
    pi_genislik = fields.Integer(string="Pervaz İç Genişlik")
    pd_genislik = fields.Integer(string="Pervaz Dış Genişlik")
    pb_genislik = fields.Integer(string="Pervaz Başlık Genişlik")
    hirdavat = fields.Char(string="Hırdavat")
    image1 = fields.Image("Resim")
    image2 = fields.Image("Resim")

    toplam_kapi = fields.Char(string="Toplam Kapı Sayısı", compute ="_compute_toplam_kapi")
    kapali_toplam_kapi = fields.Char(string="Kapalı Kapı Sayısı", compute ="_compute_kapali_toplam_kapi")
    scamli_toplam_kapi = fields.Char(string="S. Camlı Kapı Sayısı", compute ="_compute_scamli_toplam_kapi")
    citacamli_toplam_kapi = fields.Char(string="Ç. Camlı Kapı Sayısı", compute ="_compute_citacamli_toplam_kapi")

    cam_citasi = fields.Integer(string="Cam Çıtası")
    klapa_citasi = fields.Integer(string="Klapa Çıtası")
    supurge_adet = fields.Integer(string="Süpürge Adeti")

    @api.depends("task_ids")
    def _compute_toplam_kapi(self):
        tasks = self.task_ids
        gorevler = [gorev for gorev in tasks if gorev.stage_id.name == "satırlar"]
        toplam_adet = 0
        for i in gorevler:
            toplam_adet += i.adet

        for record in self:
            record.toplam_kapi =  str(toplam_adet)

    @api.depends("task_ids")
    def _compute_kapali_toplam_kapi(self):
        tasks = self.task_ids
        kapalilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":
                if gorev.tip == "1":
                    kapalilar.append(gorev)

        toplam_adet = 0
        for i in kapalilar:
            toplam_adet += i.adet

        for record in self:
            record.kapali_toplam_kapi = str(toplam_adet)



    @api.depends("task_ids")
    def _compute_scamli_toplam_kapi(self):
        tasks = self.task_ids
        scamlilar = []
        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":

                if gorev.tip == "3":
                    scamlilar.append(gorev)

        toplam_adet = 0
        for i in scamlilar:
            toplam_adet += i.adet

        for record in self:
            record.scamli_toplam_kapi = str(toplam_adet)


    @api.depends("task_ids")
    def _compute_citacamli_toplam_kapi(self):
        tasks = self.task_ids
        citalicamlilar = []

        for gorev in tasks:
            if gorev.stage_id.name == "satırlar":

                if gorev.tip == "2":
                    citalicamlilar.append(gorev)

        toplam_adet = 0
        for i in citalicamlilar:
            toplam_adet += i.adet


        for record in self:
            record.citacamli_toplam_kapi = str(toplam_adet)





    def uretim_emirleri(self):
            tasks = self.task_ids

            gorevler = []
            for gorev in tasks:
                if gorev.stage_id.name == "satırlar":
                    gorevler.append(gorev)

            return  gorevler


    def _sarim_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id


        gorevler = []
        for gorev in tasks:


            if gorev.stage_id.id == sarma_emri_stage_id:
                gorevler.append(gorev)

        return gorevler

    def _plastik_yuzey_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id


        gorevler = []
        for gorev in tasks:


            if gorev.stage_id.id == sarma_emri_stage_id and 'YÜZEY' in gorev.name and gorev.plastik=='1':
                gorevler.append(gorev)

        return gorevler

    def _mdf_yuzey_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id



        gorevler = []
        for gorev in tasks:

            if gorev.stage_id.id == sarma_emri_stage_id and 'YÜZEY' in gorev.name and gorev.plastik == '2':
                gorevler.append(gorev)

        return gorevler


    def _pervaz_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id



        gorevler = []
        for gorev in tasks:


            if gorev.stage_id.id == sarma_emri_stage_id and 'PERVAZ' in gorev.name:
                gorevler.append(gorev)

        return gorevler

    def _kas_emirleri_getir(self):

        tasks = self.task_ids
        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id

        print(sarma_emri_stage_id)

        gorevler = []
        for gorev in tasks:


            if gorev.stage_id.id == sarma_emri_stage_id and 'KASA' in gorev.name:
                gorevler.append(gorev)

        return gorevler


    def _catim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id:
                gorevler.append(gorev)
        return gorevler


    def _plastik_catim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '1' and gorev.plastik == '1':
                gorevler.append(gorev)
        return gorevler


    def _mdf_catim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '1' and gorev.plastik == '2' :
                gorevler.append(gorev)
        return gorevler


    def _plastik_kesim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '2' and gorev.plastik == '1' :
                gorevler.append(gorev)
        return gorevler

    def _mdf_kesim_emirleri_getir(self):

        tasks = self.task_ids
        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = []
        for gorev in tasks:
            if gorev.stage_id.id == catim_emri_stage_id and gorev.gorev_turu == '2' and gorev.plastik == '2':
                gorevler.append(gorev)
        return gorevler

    def cam_citalari_getir(self):

        """
        1- cam_citasini çıtalı camlıların adedi ile çarp
        2- klapa_citasi çıtalı camlıalrın adeti ile çarp
        3- en>100 olan çıtalı camlıların adetini 2 ile çarp bini_citasi yap
        4- toplam süpürge adetini direk yaz

        """

        gorevler = self.uretim_emirleri()
        citali_gorevler = [gorev for gorev in gorevler if gorev.tip == "2"]
        citali_kapi_adeti = 0
        for kapi in citali_gorevler:
            citali_kapi_adeti += kapi.adet

        cam_cita_adet = self.cam_citasi * citali_kapi_adeti
        klapa_adet = self.klapa_citasi * citali_kapi_adeti

        buyuk_yuz_gorevler = [gorev for gorev in citali_gorevler if gorev.en > 100]
        bini_cita_adet = 0
        for kapi in buyuk_yuz_gorevler:
            bini_cita_adet += kapi.adet
        bini_cita_adet = bini_cita_adet * 2

        liste = [cam_cita_adet,klapa_adet, bini_cita_adet ]
        dict = { 'cam_cita_adet': cam_cita_adet, 'klapa_adet' : klapa_adet, 'bini_cita_adet' : bini_cita_adet }
        print("asa")
        print(dict, liste)
        print("asa")
        return liste


    def kasa_emirleri(self, gorevler, sarma_emri_stage_id, plastik):

        kucukenli_gorevler = []
        buyukenli_gorevler = []

        for gorev in gorevler:
            if gorev.en > 100:
                buyukenli_gorevler.append(gorev)
            else:
                kucukenli_gorevler.append(gorev)

        kucukenli_kasa_boylari = set([a.kasa_eni for a in kucukenli_gorevler])
        buyukenli_kasa_boylari = set([a.kasa_eni for a in buyukenli_gorevler])

        kucuk_adetler = []

        for boy in kucukenli_kasa_boylari:
            adet = 0
            for gorev in kucukenli_gorevler:

                if gorev.kasa_eni == boy:
                    adet += gorev.adet
            kucuk_adetler.append([boy, adet])

        buyuk_adetler = []

        for boy in buyukenli_kasa_boylari:
            adet = 0
            for gorev in buyukenli_gorevler:
                print(gorev.kasa_eni, gorev.adet)

                if gorev.kasa_eni == boy:
                    adet += gorev.adet
            buyuk_adetler.append([boy, adet])

        for sta in kucuk_adetler:
            self.env['project.task'].create({'project_id': self.id, 'planned_hours':math.ceil(sta[1] * 2.5),
                                             'stage_id': sarma_emri_stage_id, 'plastik':plastik,
                                             'name': "KASA" + str(sta[0]) + " cm " + str(
                                                 math.ceil(sta[1] * 2.5)) + " Adet"})

        for sta in buyuk_adetler:
            self.env['project.task'].create({'project_id': self.id, 'planned_hours':math.ceil(sta[1] * 3),
                                             'stage_id': sarma_emri_stage_id, 'plastik':plastik,
                                             'name': "KASA" + str(sta[0]) + " cm " + str(
                                                 math.ceil(sta[1] * 3)) + " Adet"})



    def pervaz_emirleri(self, gorevler, sarma_emri_stage_id):

        toplam_adet = 0
        for gorev in gorevler:
            toplam_adet += gorev.adet

        pit_kalinlik = self.pit_kalinlik
        pdt_kalinlik = self.pdt_kalinlik
        pb_kalinlik = self.pb_kalinlik
        pi_genislik = self.pi_genislik
        pd_genislik = self.pd_genislik
        pb_genislik = self.pb_genislik

        if pit_kalinlik == pdt_kalinlik == pb_kalinlik and pi_genislik == pd_genislik == pb_genislik:

            self.env['project.task'].create({'project_id': self.id,'planned_hours':toplam_adet * 5,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 5) + " Adet"})



        elif pit_kalinlik == pdt_kalinlik and pi_genislik == pd_genislik:

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet * 4,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 4) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pb_kalinlik) + " cm " + str(
                                                 pb_genislik) + " mm  " + str(
                                                 toplam_adet * 1) + " Adet"})

        elif pit_kalinlik == pb_kalinlik and pi_genislik == pb_genislik:

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet * 3,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 3) + " Adet"})

            self.env['project.task'].create({'project_id': self.id,'planned_hours':toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " cm " + str(
                                                 pd_genislik) + " mm  " + str(
                                                 toplam_adet * 2) + " Adet"})



        elif pdt_kalinlik == pb_kalinlik and pd_genislik == pb_genislik:

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet * 3,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " cm " + str(
                                                 pd_genislik) + " mm  " + str(
                                                 toplam_adet * 3) + " Adet"})



        else:

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pit_kalinlik) + " cm " + str(
                                                 pi_genislik) + " mm  " + str(toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet * 2,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pdt_kalinlik) + " cm " + str(
                                                 pd_genislik) + " mm  " + str(
                                                 toplam_adet * 2) + " Adet"})

            self.env['project.task'].create({'project_id': self.id, 'planned_hours':toplam_adet,
                                             'stage_id': sarma_emri_stage_id,
                                             'name': "PERVAZ " + str(pb_kalinlik) + " cm " + str(
                                                 pb_genislik) + " mm  " + str(
                                                 toplam_adet * 1) + " Adet"})

    def yuzey_emirleri(self, gorevler, sarma_emri_stage_id, plastik):
        print(self, gorevler, sarma_emri_stage_id, plastik)

        scamli_gorevler = []
        kapali_gorevler = []

        for gorev in gorevler:
            if gorev.tip == "3":
                scamli_gorevler.append(gorev)
            elif gorev.tip == "2" or gorev.tip == "1":
                kapali_gorevler.append(gorev)

        scamli_enler = set([a.en for a in scamli_gorevler])

        scamlienadetler = []

        for boy in scamli_enler:
            adet = 0
            for gorev in scamli_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            scamlienadetler.append([boy, adet])

        for i in scamlienadetler:
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik':plastik,
                                             'name': "YÜZEY 18mm " + str(210) + " cm " + str(
                                                 i[0] - 5) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})





        kapali_enler = set([a.en for a in kapali_gorevler])

        kapaliadetler = []

        for boy in kapali_enler:
            adet = 0
            for gorev in kapali_gorevler:

                if gorev.en == boy:
                    adet += gorev.adet
            kapaliadetler.append([boy, adet])

        for i in kapaliadetler:
            self.env['project.task'].create({'project_id': self.id,'planned_hours': i[1] * 2,
                                             'stage_id': sarma_emri_stage_id, 'plastik':plastik,
                                             'name': "YÜZEY  " + str(self.yuzey_kalinlik) + " mm " + str(210) + " cm " + str(
                                                 i[0] - 4) + " cm  " + str(
                                                 i[1] * 2) + " Adet"})





    def gorev(self):
        gorevler = self.uretim_emirleri()

        sarma_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "SARMA EMRİ")], limit=1).id



        plastik = '2'
        gorevler = [gorev for gorev in gorevler if gorev.plastik == str(2)]

        self.kasa_emirleri(gorevler, sarma_emri_stage_id, plastik)
        self.pervaz_emirleri(gorevler, sarma_emri_stage_id)
        self.yuzey_emirleri(gorevler, sarma_emri_stage_id, plastik)


        plastik = '1'
        gorevler = self.uretim_emirleri()

        gorevler = [gorev for gorev in gorevler if gorev.plastik == plastik]

        self.yuzey_emirleri(gorevler, sarma_emri_stage_id, plastik)

    def kasa_ebatlama(self, gorevler, catim_emri_stage_id ):

        kasaenler = []
        for gorev in gorevler:
            kasaenler.append((gorev.kasa_eni, [gorev]))

        kasaen_gorevler = {}

        for item in kasaenler:

            if item[0] in kasaen_gorevler:
                kasaen_gorevler[item[0]].append(item[1][0])
            else:
                kasaen_gorevler[item[0]] = item[1]

        ebatlama_gorevler = []

        for item in kasaen_gorevler:
            for i in kasaen_gorevler[item]:
                gr = str(i.kasa_eni) + " mm " + str(i.boy) + " cm x " + str(i.en) + " cm "
                ebatlama_gorevler.append((gr, [i.adet]))

        ebatlama_gorevler_dict = {}

        for item in ebatlama_gorevler:

            if item[0] in ebatlama_gorevler_dict:
                ebatlama_gorevler_dict[item[0]].append(item[1][0])
            else:
                ebatlama_gorevler_dict[item[0]] = item[1]

        for item in ebatlama_gorevler_dict:
            ebatlama_gorevler_dict[item] = sum(ebatlama_gorevler_dict[item])

        for key in ebatlama_gorevler_dict:
            gorev_adi = key + str(ebatlama_gorevler_dict[key]) + " Adet"
            gorev_adet =  ebatlama_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_adet,
                                             'stage_id': catim_emri_stage_id,
                                             'name': gorev_adi})


    def tip_degeri_bul(self, tip):
        return dict(self.env["project.task"].fields_get(allfields=["tip"])["tip"]['selection'])[tip]




    def catim_emri(self):

        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler  if gorev.tip in ['1','2'] and gorev.plastik =='2' ]


        kapali_gorevler_adetli = []

        for gorev in kapali_gorevler:
            gorev_adi = str(self.tip_degeri_bul(gorev.tip)) + " : " + str(gorev.boy-3) + " cm " + \
                        str(gorev.en-5) + " cm : "
            adet=gorev.adet
            kapali_gorevler_adetli.append([gorev_adi, [adet]])

        kapali_gorevler_dict = {}

        for item in kapali_gorevler_adetli:

            if item[0] in kapali_gorevler_dict:
                kapali_gorevler_dict[item[0]].append(item[1][0])
            else:
                kapali_gorevler_dict[item[0]] = item[1]

        for item in kapali_gorevler_dict:
            kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        for key in kapali_gorevler_dict:
            gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
            gorev_Adet = kapali_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours':gorev_Adet,
                                             'stage_id': catim_emri_stage_id, 'plastik' : '2',
                                         'gorev_turu':'1', 'name': gorev_adi})

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler if gorev.tip in ['1','2'] and gorev.plastik == '1']

        kapali_gorevler_adetli = []

        for gorev in kapali_gorevler:
            gorev_adi = str(self.tip_degeri_bul(gorev.tip)) + " : " + str(gorev.boy - 3) + " cm " + \
                        str(gorev.en - 5) + " cm : "

            adet = gorev.adet
            kapali_gorevler_adetli.append([gorev_adi, [adet]])

        kapali_gorevler_dict = {}

        for item in kapali_gorevler_adetli:

            if item[0] in kapali_gorevler_dict:
                kapali_gorevler_dict[item[0]].append(item[1][0])
            else:
                kapali_gorevler_dict[item[0]] = item[1]

        for item in kapali_gorevler_dict:
            kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        for key in kapali_gorevler_dict:
            gorev_adi = key + str(kapali_gorevler_dict[key]) + " Adet"
            gorev_Adet = kapali_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_Adet,
                                             'stage_id': catim_emri_stage_id, 'plastik': '1',
                                             'gorev_turu':'1', 'name': gorev_adi})


        self.kesim_emri()


    def kesim_emri(self):

        catim_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "ÇATIM EMRİ")], limit=1).id

        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler  if gorev.tip in ['1', '2'] and gorev.plastik =='2' ]

        kapali_gorevler_adetli = []

        for gorev in kapali_gorevler:
            gorev_adi = str(gorev.kasa_eni) + " x " +  str(gorev.boy) + " x " + str(gorev.en)
            adet = gorev.adet
            kapali_gorevler_adetli.append([gorev_adi, [adet]])

        kapali_gorevler_dict = {}

        for item in kapali_gorevler_adetli:

            if item[0] in kapali_gorevler_dict:
                kapali_gorevler_dict[item[0]].append(item[1][0])
            else:
                kapali_gorevler_dict[item[0]] = item[1]

        for item in kapali_gorevler_dict:
            kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        for key in kapali_gorevler_dict:
            gorev_adi = key + " : " + str(kapali_gorevler_dict[key]) + " Adet"
            gorev_Adet = kapali_gorevler_dict[key]


            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_Adet,
                                             'stage_id': catim_emri_stage_id, 'plastik': '2',
                                              'gorev_turu':'2', 'name': gorev_adi})




        gorevler = self.uretim_emirleri()
        kapali_gorevler = [gorev for gorev in gorevler if gorev.tip in ['1', '2'] and gorev.plastik == '1']

        kapali_gorevler_adetli = []

        for gorev in kapali_gorevler:
            gorev_adi = str(gorev.kasa_eni) + " x " + str(gorev.boy) + " x " + str(gorev.en)
            adet = gorev.adet
            kapali_gorevler_adetli.append([gorev_adi, [adet]])

        kapali_gorevler_dict = {}

        for item in kapali_gorevler_adetli:

            if item[0] in kapali_gorevler_dict:
                kapali_gorevler_dict[item[0]].append(item[1][0])
            else:
                kapali_gorevler_dict[item[0]] = item[1]

        for item in kapali_gorevler_dict:
            kapali_gorevler_dict[item] = sum(kapali_gorevler_dict[item])

        for key in kapali_gorevler_dict:
            gorev_adi = key + " : " + str(kapali_gorevler_dict[key]) + " Adet"
            gorev_Adet = kapali_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_Adet,
                                             'stage_id': catim_emri_stage_id, 'plastik': '1',
                                             'gorev_turu':'2', 'name': gorev_adi})

    def plastik_emri(self):

        gorevler = self.uretim_emirleri()

        plastik_emri_stage_id = self.env['project.task.type'].search(
            [('project_ids', 'in', self.id), ('name', 'like', "PLASTİK EMRİ")], limit=1).id


        plastik_gorevler = [gorev for gorev in gorevler  if gorev.plastik == "1" ]

        pop_gorevler = []
        pap_gorevler = []
        pbpo_gorevler = []
        pbpa_gorevler = []


        for gorev in plastik_gorevler:
            gorev_pop = str(gorev.pop.name)
            gorev_pap = str(gorev.pap.name)
            gorev_pbpo = str(gorev.pbpo.name)
            gorev_pbpa = str(gorev.pbpa.name)

            adet=gorev.adet
            pop_gorevler.append([gorev_pop, [adet]])
            pap_gorevler.append([gorev_pap, [adet]])
            pbpo_gorevler.append([gorev_pbpo, [adet]])
            pbpa_gorevler.append([gorev_pbpa, [adet]])


        pop_gorevler_dict = {}
        for item in pop_gorevler:
            if item[0] in pop_gorevler_dict:
                pop_gorevler_dict[item[0]].append(item[1][0])
            else:
                pop_gorevler_dict[item[0]] = item[1]

        for item in pop_gorevler_dict:
            pop_gorevler_dict[item] = sum(pop_gorevler_dict[item])

        for key in pop_gorevler_dict:
            gorev_adi = key + " x  " +  str(pop_gorevler_dict[key] * 2) + " Adet"
            gorev_Adet = pop_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours':gorev_Adet,
                                             'stage_id': plastik_emri_stage_id,
                                         'name': gorev_adi})

        pap_gorevler_dict = {}
        for item in pap_gorevler:
            if item[0] in pap_gorevler_dict:
                pap_gorevler_dict[item[0]].append(item[1][0])
            else:
                pap_gorevler_dict[item[0]] = item[1]

        for item in pap_gorevler_dict:
            pap_gorevler_dict[item] = sum(pap_gorevler_dict[item])

        for key in pap_gorevler_dict:
            gorev_adi = key + " x  " + str(pap_gorevler_dict[key] * 2) + " Adet"
            gorev_Adet = pap_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_Adet,
                                             'stage_id': plastik_emri_stage_id,
                                             'name': gorev_adi})

        pbpo_gorevler_dict = {}
        for item in pbpo_gorevler:
            if item[0] in pbpo_gorevler_dict:
                pbpo_gorevler_dict[item[0]].append(item[1][0])
            else:
                pbpo_gorevler_dict[item[0]] = item[1]

        for item in pbpo_gorevler_dict:
            pbpo_gorevler_dict[item] = sum(pbpo_gorevler_dict[item])

        for key in pbpo_gorevler_dict:
            gorev_adi = key + " x  " + str(math.ceil(pbpo_gorevler_dict[key] * 0.5)) + " Adet"
            gorev_Adet = pbpo_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_Adet,
                                             'stage_id': plastik_emri_stage_id,
                                             'name': gorev_adi})

        pbpa_gorevler_dict = {}
        for item in pbpa_gorevler:
            if item[0] in pbpa_gorevler_dict:
                pbpa_gorevler_dict[item[0]].append(item[1][0])
            else:
                pbpa_gorevler_dict[item[0]] = item[1]

        for item in pbpa_gorevler_dict:
            pbpa_gorevler_dict[item] = sum(pbpa_gorevler_dict[item])

        for key in pbpa_gorevler_dict:
            gorev_adi = key + " x  " + str(math.ceil(pbpa_gorevler_dict[key] * 0.5)) + " Adet"
            gorev_Adet = pbpa_gorevler_dict[key]
            self.env['project.task'].create({'project_id': self.id, 'planned_hours': gorev_Adet,
                                             'stage_id': plastik_emri_stage_id,
                                             'name': gorev_adi})







class ProjectTask(models.Model):

    _inherit = 'project.task'
    _description = 'Task inherit'

    kasa_eni = fields.Integer(string="Kasa", default=1.0)
    en = fields.Integer(string="En", default=1.0)
    boy = fields.Integer(string="Boy", default=1.0)
    adet = fields.Integer(string="Adet", default=1.0)


    tip = fields.Selection([
        ('1', 'Kapalı'),
        ('2', 'Çıtalı Camlı'),
        ('3', 'Salma Camlı'),
        ('4', 'kanat Yok '),
    ],  string="Tip")

    plastik = fields.Selection([
        ('1', 'Evet'),
        ('2', 'Hayır'),
    ], default='2', string="Plastik mi?")

    gorev_turu = fields.Selection([
        ('1', 'catim'),
        ('2', 'kesim'),
        ('3', 'kasa'),
        ('4', 'pervaz'),
        ('5', 'yuzey'),
    ], default='1', string="gorev turu?")

    oda =  fields.Many2one('yaman.oda',string="Oda")
    pop =  fields.Many2one('yaman.plastik',string="Plastik Ön Peraz")
    pap =  fields.Many2one('yaman.plastik',string="Plastik Arka Peraz")
    pbpo =  fields.Many2one('yaman.plastik',string="Plastik Başlık Peraz Ön")
    pbpa =  fields.Many2one('yaman.plastik',string="Plastik Başlık Peraz Arka")

    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Status',
        copy=False, default='normal', required=True,  readonly=False, store=True)

    kanban_state_label = fields.Char(compute='_compute_kanban_state_label', string='Kanban State Label', tracking=True,
                                     task_dependency_tracking=True)




    @api.depends('kanban_state_label')
    def _onchange_kanban_state_label(self):
        print(self.kanban_state)
        raise UserWarning("sd")

    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == 'normal':
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == 'blocked':
                task.kanban_state_label = task.legend_blocked
            else:
                task.kanban_state_label = task.legend_done



    def actipn_sarim_emri(self):
        print("basari")



