from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Tavara, Hanke
from . import db
from flask_login import login_required, current_user
from .forms import NewItem, EditItem
from datetime import datetime


views = Blueprint('views', __name__)

#Tällä funktiolla hallitaan stringien, jotka näytetään dropdownissa, maksimipituutta
def truncate_string(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    else:
        return text

#Tämä ajetaan, kun käyttäjä vierailee kotisivulla/tietokannan selailunäkymässä
@views.route('/')
@login_required
def home():
    all_items = Tavara.query.all()

    items_truncated = all_items
    if items_truncated:
        for item in items_truncated:
            item.tavaraNimi = truncate_string(item.tavaraNimi, 20)
            item.tavaraMalli = truncate_string(item.tavaraMalli, 20)
            item.tavaraValmistaja = truncate_string(item.tavaraValmistaja, 20)

    return render_template("data2.html", all_items=items_truncated, current_user=current_user)

#Tämä ajetaan, kun poistetaan käyttäjän valitsema tavara tietokannasta
@views.route('/deleted', methods=['GET', 'POST'])
@login_required
def deleted():
    item_id = request.form.get('itemID')

    item_to_be_deleted = Tavara.query.get(item_id)
    if item_to_be_deleted:
        db.session.delete(item_to_be_deleted)
        try:
            db.session.commit()

            flash('Tavara poistettu!', 'success_data')
            return redirect(url_for('views.home'))
        except Exception as e:
            flash('Ei voitu kirjoittaa tietokantaan.', 'error')
            return redirect(url_for('views.home'))
    
    else:
        flash('Tavaraa ei löytynyt.', 'error')
        return redirect(url_for('views.home'))

#Tämä ajetaan, kun käyttäjä klikkaa kotisivulla/tietokannan selailunäkymässä "Luo uusi"
#Tällä voidaan siis luoda uusi tavara, ja joko luoda uusi hanke johon tavara kuuluu, tai käyttää jo olemassaolevaa hanketta
@views.route('/create_new', methods=['GET', 'POST'])
@login_required
def create_new():
    form = NewItem()

    projects = Hanke.query.all()

    select_list = []

    projects_truncated = projects
    if projects_truncated:
        for project in projects_truncated:
            project.hankeNimi = truncate_string(project.hankeNimi, 20)
            project.projektiPäällikkö = truncate_string(project.projektiPäällikkö, 20)
            project.aloitusPvm = truncate_string(project.aloitusPvm, 20)
            project.loppumisPvm = truncate_string(project.loppumisPvm, 20)
            select_list.append((project.hankeID, f"{project.hankeNimi} | {project.projektiPäällikkö} | {project.aloitusPvm} | {project.loppumisPvm}"))

    if select_list:
        form.select.choices = select_list
    else:
        form.select.choices = [("", "Ei hankkeita")]
        
    if request.method == 'POST' and form.new_or_old.data == "new" and form.validate_on_submit():
        
        name = form.item_name.data
        model = form.item_model.data
        manufacturer = form.item_manufacturer.data
        canBeThrownAway = form.can_be_thrown_away.data.strftime('%d/%m/%Y')
        warranty = form.warranty.data.strftime('%d/%m/%Y')
        ownerName = form.owner_name.data
        ownerEmail = form.owner_email.data
        userName = form.user_name.data
        userEmail = form.user_email.data

        projectName = form.project_name.data
        projectManager = form.project_manager.data
        startDate = form.start_date.data.strftime('%d/%m/%Y')
        endDate = form.end_date.data.strftime('%d/%m/%Y')

        new_project = Hanke(hankeNimi = projectName, projektiPäällikkö = projectManager, aloitusPvm = startDate, loppumisPvm = endDate)
        db.session.add(new_project)
        try:
            db.session.commit()

            latestProject = Hanke.query.order_by(Hanke.hankeID.desc()).first()
            
            projectID = latestProject.hankeID

            new_item = Tavara(hankeID = projectID, tavaraNimi = name, tavaraMalli = model, tavaraValmistaja = manufacturer, voidaanHeittääPoisAikaisintaan = canBeThrownAway, takuuPäättyy = warranty, omistajaNimi = ownerName, omistajaSähköposti = ownerEmail, käyttäjäNimi = userName, käyttäjäSähköposti = userEmail)
            db.session.add(new_item)
            try:
                db.session.commit()

                flash('Uusi tavara luotu!', 'success_data')
                return redirect(url_for('views.home'))
            except Exception as e:
                flash('Ei voitu kirjoittaa tietokantaan.', 'error')
                return redirect(url_for('views.home'))
        except Exception as e:
            flash('Ei voitu kirjoittaa tietokantaan.', 'error')
            return redirect(url_for('views.home'))

    elif request.method == 'POST' and form.new_or_old.data == "not-new" and form.validate_on_submit():
        name = form.item_name.data
        model = form.item_model.data
        manufacturer = form.item_manufacturer.data
        canBeThrownAway = form.can_be_thrown_away.data.strftime('%d/%m/%Y')
        warranty = form.warranty.data.strftime('%d/%m/%Y')
        ownerName = form.owner_name.data
        ownerEmail = form.owner_email.data
        userName = form.user_name.data
        userEmail = form.user_email.data

        projectID = form.select.data

        new_item = Tavara(hankeID = projectID, tavaraNimi = name, tavaraMalli = model, tavaraValmistaja = manufacturer, voidaanHeittääPoisAikaisintaan = canBeThrownAway, takuuPäättyy = warranty, omistajaNimi = ownerName, omistajaSähköposti = ownerEmail, käyttäjäNimi = userName, käyttäjäSähköposti = userEmail)
        db.session.add(new_item)
        try:
            db.session.commit()
            flash('Uusi tavara luotu!', 'success_data')
            return redirect(url_for('views.home'))
        except Exception as e:
            flash('Ei voitu kirjoittaa tietokantaan.', 'error')
            return redirect(url_for('views.home'))


    return render_template("create_new2.html", projects=projects_truncated, form=form)

#Tämä ajetaan, kun käyttäjä klikkaa kotisivulla/tietokannan selailunäkymässä 'Lisätietoja/Muokkaa'
#Tällä siis haetaan valitun tavaran tiedot katsottavaksi ja muokattavaksi
@views.route('/info_edit', methods=['GET', 'POST'])
@login_required
def info_edit():
    item_id = request.args.get('id')

    item = Tavara.query.get(item_id)

    if item:
        project_id = item.hankeID
        project = Hanke.query.get(project_id)
    else:
        flash('Tavaraa ei löytynyt.', 'error')
        return redirect(url_for('views.home'))
    
    if request.method == "POST":
        form = EditItem()
    else:
        try:
            form = EditItem(obj=item)
            form.item_name.data = item.tavaraNimi
            form.item_model.data = item.tavaraMalli
            form.item_manufacturer.data = item.tavaraValmistaja
            form.can_be_thrown_away.data = datetime.strptime(item.voidaanHeittääPoisAikaisintaan, '%d/%m/%Y').date()
            form.warranty.data = datetime.strptime(item.takuuPäättyy, '%d/%m/%Y').date()

            form.owner_name.data = item.omistajaNimi
            form.owner_email.data = item.omistajaSähköposti

            form.user_name.data = item.käyttäjäNimi
            form.user_email.data = item.käyttäjäSähköposti

            form.project_name.data = project.hankeNimi
            form.project_manager.data = project.projektiPäällikkö
            form.start_date.data = datetime.strptime(project.aloitusPvm, '%d/%m/%Y').date()
            form.end_date.data = datetime.strptime(project.loppumisPvm, '%d/%m/%Y').date()
        except Exception as e:
            print(e)
            flash('Tietojen lataaminen ei onnistu.', 'error')
            return redirect(url_for('views.home'))
    
    if request.method == 'POST' and form.validate_on_submit():

        updated_name = form.item_name.data
        updated_model = form.item_model.data
        updated_manufacturer = form.item_manufacturer.data
        updated_canBeThrownAway = form.can_be_thrown_away.data.strftime('%d/%m/%Y')
        updated_warranty = form.warranty.data.strftime('%d/%m/%Y')
        updated_ownerName = form.owner_name.data
        updated_ownerEmail = form.owner_email.data
        updated_userName = form.user_name.data
        updated_userEmail = form.user_email.data

        updated_projectName = form.project_name.data
        updated_projectManager = form.project_manager.data
        updated_startDate = form.start_date.data.strftime('%d/%m/%Y')
        updated_endDate = form.end_date.data.strftime('%d/%m/%Y')
        

        if item and project:
            item.tavaraNimi = updated_name
            item.tavaraMalli = updated_model
            item.tavaraValmistaja = updated_manufacturer
            item.voidaanHeittääPoisAikaisintaan = updated_canBeThrownAway
            item.takuuPäättyy = updated_warranty
            item.omistajaNimi = updated_ownerName
            item.omistajaSähköposti = updated_ownerEmail
            item.käyttäjäNimi = updated_userName
            item.käyttäjäSähköposti = updated_userEmail
            project.hankeNimi = updated_projectName
            project.projektiPäällikkö = updated_projectManager
            project.aloitusPvm = updated_startDate
            project.loppumisPvm = updated_endDate
            try:
                db.session.commit()

                flash('Muutokset tallennettu tietokantaan!', 'success_data')
                return redirect(url_for('views.home'))
            except Exception as e:
                flash('Ei voitu kirjoittaa tietokantaan.', 'error')
                return redirect(url_for('views.home'))
        else:
            flash('Jotakin meni vikaan', 'error')
            return redirect(url_for('views.home'))
    
    if item:
        return render_template('info_edit2.html', form=form)
    else:
        flash('Tavaraa ei löytynyt.', 'error')
        return redirect(url_for('views.home'))
    
