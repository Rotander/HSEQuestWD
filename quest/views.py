import csv
from django.http import Http404, HttpResponse
from django.shortcuts import render
from quest.models import CorrectPageAnswer, FeedBack
from quest.models import PageAnswer, PageHint, Quest, QuestPage
from quest.models import PageParagraph
from user.models import Game, User

HINT_COST = 5
ANSWER_REWARD = 10


def index(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    return render(request, 'index.html', {'user': request.user, })


def catalog(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    return render(
        request,
        'catalog.html',
        {
            'quest_list': Quest.objects.all(),
            'user': request.user,
        })


def new_play(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    user = request.user
    res = {
        'user': user
    }
    # get the user language, default is rus
    lang = request.session.get('lang', 0)

    if not user.is_authenticated:
        return render(request, 'forbidden.html', res)
    if 'q_id' in request.GET:
        q_id = request.GET['q_id']
    else:
        raise Http404
    if 'ans' in request.POST:
        u_ans = request.POST['ans']
    else:
        u_ans = ''

    if Quest.objects.filter(id=q_id):
        quest = Quest.objects.filter(id=q_id)[0]
    else:
        raise Http404
    if Game.objects.filter(profile=user, quest=quest):
        game = Game.objects.filter(profile=user, quest=quest)[0]
    else:
        game = Game(profile=user, quest=quest, last_page=0)
        game.save()

    page_num = game.last_page
    pages = QuestPage.objects.filter(quest=quest)
    quest_size = len(pages)
    page = pages[page_num]
    # if lang is eng
    if lang:
        answers = [
            ans.page_answer_en for ans in PageAnswer.objects.filter(
                quest_page=page)]

        correct_answer = CorrectPageAnswer.objects.filter(
            quest_page=page
        )
        if len(correct_answer) == 0:
            correct_answer = "Undefined"
        else:
            correct_answer = correct_answer[0].correct_page_answer_en

    # if lang is rus
    else:
        answers = [
            ans.page_answer_ru for ans in PageAnswer.objects.filter(
                quest_page=page)]

        correct_answer = CorrectPageAnswer.objects.filter(
            quest_page=page
        )
        if len(correct_answer) == 0:
            correct_answer = "Undefined"
        else:
            correct_answer = correct_answer[0].correct_page_answer_ru

    # if an user wants to move without answering
    if 'forced_move' in request.POST:
        # we want to response with the next page so we need to update vars
        # but if it was last page of the quest we don't want to
        if game.last_page != quest_size - 1:
            game.last_page += 1
        game.save()
        page_num = game.last_page
        page = pages[page_num]
        # if lang is eng
        if lang:
            answers = [
                ans.page_answer_en for ans in PageAnswer.objects.filter(
                    quest_page=page)]
            correct_answer = CorrectPageAnswer.objects.filter(
                quest_page=page
            )
            if len(correct_answer) == 0:
                correct_answer = "Undefined"
            else:
                correct_answer = correct_answer[0].correct_page_answer_en
        # if lang is rus
        else:
            answers = [
                ans.page_answer_ru for ans in PageAnswer.objects.filter(
                    quest_page=page)]

            correct_answer = CorrectPageAnswer.objects.filter(
                quest_page=page
            )
            if len(correct_answer) == 0:
                correct_answer = "Undefined"
            else:
                correct_answer = correct_answer[0].correct_page_answer_ru

    # if an user wants to move to the next page
    move_request = 'move' in request.POST
    # check if the given answer's correct
    ans_correct = any(ans in u_ans.lower() for ans in answers)
    if move_request and (ans_correct or answers == []):
        if ans_correct:
            user.pts += ANSWER_REWARD
            user.save()
        # we want to response with the next page so we need to update vars
        # but if it was last page of the quest we don't want to
        if game.last_page != quest_size - 1:
            game.last_page += 1
        game.save()
        page_num = game.last_page
        page = pages[page_num]
        # if lang is eng
        if lang:
            answers = [
                ans.page_answer_en for ans in PageAnswer.objects.filter(
                    quest_page=page)]
            correct_answer = CorrectPageAnswer.objects.filter(
                quest_page=page
            )
            if len(correct_answer) == 0:
                correct_answer = "Undefined"
            else:
                correct_answer = correct_answer[0].correct_page_answer_en
        # if lang is rus
        else:
            answers = [
                ans.page_answer_ru for ans in PageAnswer.objects.filter(
                    quest_page=page)]
            correct_answer = CorrectPageAnswer.objects.filter(
                quest_page=page
            )
            if len(correct_answer) == 0:
                correct_answer = "Undefined"
            else:
                correct_answer = correct_answer[0].correct_page_answer_ru
    # if the answer was sent but wrong
    elif move_request:
        res['wrong'] = True

    # get hints and separate them into bought and remaining
    all_bought_hints = game.bought_hints.all()
    rem_hints = []
    hints = []
    for hint in PageHint.objects.filter(quest_page=page):
        if hint in all_bought_hints:
            hints.append(hint)
        else:
            rem_hints.append(hint)

    # check if hints were requested
    if 'hint' in request.POST:
        user.pts -= HINT_COST
        user.save()
        game.bought_hints.add(rem_hints[int(request.POST['hint']) - 1])
        hints.append(rem_hints.pop(int(request.POST['hint']) - 1))
        game.save()

    # create a response
    res['answer_ex'] = answers != []
    res['hints'] = hints
    res['rem_hints'] = range(1, len(rem_hints) + 1)
    res['page_num'] = page_num + 1
    res['quest_length'] = quest_size
    res['page'] = page
    res['q_id'] = q_id
    res['end_of_the_quest'] = page_num == (quest_size - 1)
    res['preend_of_quest'] = page_num == (quest_size - 2)
    res['paragraphs'] = PageParagraph.objects.filter(page=page)
    res['correct_answer'] = correct_answer

    return render(request, 'play.html', res)


def feedback(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)

    user = request.user

    if 'q_id' in request.GET:
        q_id = int(request.GET['q_id'])
    else:
        raise Http404

    res = {
        'user': user,
        'q_id': q_id,
    }

    res['feedback_send'] = bool(FeedBack.objects.filter(
        user_name=str(user), q_id=q_id))

    if request.POST and not res['feedback_send']:

        feedback = FeedBack(
            q_id=q_id,
            user_name=str(user),
            convenience=int(request.POST.get('convenience', -1)),
            complexity=int(request.POST.get('complexity', -1)),
            text_quality=int(request.POST.get('text_quality', -1)),
            what_to_delete=request.POST.get('what_to_delete', '.'),
            what_to_add=request.POST.get('what_to_add', '.'),
            did_quest_help=int(request.POST.get('did_quest_help', -1)),
            recommendation=int(request.POST.get('recommendation', -1)),
            why_such_ans=request.POST.get('why_such_ans', '.'),
            rate=int(request.POST.get('rate', -1)),
            )
        feedback.save()
        res['feedback_send'] = True

    return render(request, 'feedback.html', res)


def aboutus(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    return render(request, 'aboutus.html', {'user': request.user, })


def export_users_pages_csv(request):
    if not request.user.is_superuser:
        return render(request, 'forbidden.html')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'email',
        'last_page',
        ])

    quest = Quest.objects.filter(id=1)[0]
    users = User.objects.all()
    exp = []
    for user in users:
        if Game.objects.filter(profile=user, quest=quest):
            game = Game.objects.filter(profile=user, quest=quest)[0]
        else:
            continue
        exp.append([user.email, game.last_page + 1])

    for e in exp:
        writer.writerow(e)

    return response


def export_finished_users_csv(request):
    if not request.user.is_superuser:
        return render(request, 'forbidden.html')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'email',
        ])

    quest = Quest.objects.filter(id=1)[0]
    users = User.objects.all()
    for user in users:
        if Game.objects.filter(profile=user, quest=quest):
            game = Game.objects.filter(profile=user, quest=quest)[0]
        else:
            continue
        if game.last_page + 1 == len(QuestPage.objects.filter(quest=quest)):
            writer.writerow([user.email])

    return response


def export_feedback_csv(request):
    if not request.user.is_superuser:
        return render(request, 'forbidden.html')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'q_id',
        'convenience',
        'complexity',
        'text_quality',
        'what_to_delete',
        'what_to_add',
        'did_quest_help',
        'recommendation',
        'why_such_ans',
        'rate',
    ])

    feedbacks = FeedBack.objects.all().values_list(
        'q_id',
        'convenience',
        'complexity',
        'text_quality',
        'what_to_delete',
        'what_to_add',
        'did_quest_help',
        'recommendation',
        'why_such_ans',
        'rate',
        )
    for feedback in feedbacks:
        writer.writerow(feedback)

    return response
