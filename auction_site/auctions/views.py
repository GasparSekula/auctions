from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AuctionItem, Bid, Notification
from .forms import AuctionItemForm, BidForm
from django.db.models import Q, Max
from django.utils import timezone
from .serializers import AuctionSerializer
from rest_framework import viewsets
import csv
import xml.etree.ElementTree as ET
from django.http import HttpResponse, JsonResponse
from decimal import Decimal, InvalidOperation


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionSerializer


def handler_400(request, exception):
    return render(request, '400.html', status=400)


def handler_403(request, exception):
    return render(request, '403.html', status=403)


def handler_404(request, exception):
    return render(request, '404.html', status=404)


def handler_500(request):
    return render(request, '500.html', status=500)


def home(request):
    total_auctions = AuctionItem.objects.count()
    active_auctions = sum(1 for auction in AuctionItem.objects.all() if auction.is_active)
    most_expensive_auction = AuctionItem.objects.aggregate(Max('current_price'))['current_price__max']

    return render(request, 'auctions/home.html', {
        'total_auctions': total_auctions,
        'active_auctions': active_auctions,
        'most_expensive_auction': most_expensive_auction,
    })


def auction_list(request):
    auctions = AuctionItem.objects.all()

    # show closed
    show_closed = request.GET.get('show_closed', 'off') == 'on'
    if not show_closed:
        auctions = auctions.filter(auction_end_date__gt=timezone.now())

    # filter by date
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        auctions = auctions.filter(auction_end_date__gte=date_from)
    if date_to:
        auctions = auctions.filter(auction_end_date__lte=date_to)

    # filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        auctions = auctions.filter(current_price__gte=min_price)
    if max_price:
        auctions = auctions.filter(current_price__lte=max_price)

    # only with image
    show_with_image = request.GET.get('show_with_image', 'off') == 'on'
    if show_with_image:
        auctions = auctions.filter(image__isnull=False)

    # sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price':
        auctions = auctions.order_by('current_price')
    elif sort_by == '-price':
        auctions = auctions.order_by('-current_price')
    elif sort_by == 'date':
        auctions = auctions.order_by('auction_end_date')
    elif sort_by == '-date':
        auctions = auctions.order_by('-auction_end_date')

    return render(request, 'auctions/auction_list.html', {'auctions': auctions})


@login_required
def auction_detail(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)
    form = BidForm(request.POST or None)
    error_messages = []

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount', '0')

        try:
            # Ensure bid amount is treated as a decimal with two decimal places
            bid_amount = Decimal(bid_amount).quantize(Decimal('0.01'))

            # Ensure bid amount is not lower than current price
            if bid_amount <= auction.current_price:
                error_messages.append("Your bid must be higher than the current price.")
            else:
                # Check for precision and size: Max 8 digits before decimal and 2 decimal places
                bid_amount_str = str(bid_amount)
                if len(bid_amount_str.split('.')[0]) > 8:  # Integer part exceeds 8 digits
                    error_messages.append("Bid amount cannot exceed 8 digits before the decimal.")
                if len(bid_amount_str.split('.')[1]) > 2:  # Decimal part exceeds 2 digits
                    error_messages.append("Bid amount cannot have more than 2 decimal places.")

        except InvalidOperation:
            error_messages.append("Invalid bid amount. Please enter a valid number.")

        if not error_messages:
            # If all validation passes, save the bid
            auction.current_price = bid_amount
            auction.save()

            # Create a new bid entry
            bid = Bid.objects.create(
                auction_item=auction,
                user=request.user,
                amount=bid_amount
            )

            # Notify the previous highest bidder if applicable
            previous_highest_bid = auction.bids.order_by('-amount').exclude(pk=bid.pk).first()
            if previous_highest_bid:
                Notification.objects.create(
                    user=previous_highest_bid.user,
                    message=f"You've been outbid on auction '{auction.title}'."
                )

            # Notify the auction creator
            Notification.objects.create(
                user=auction.created_by,
                message=f"A new bid has been placed on your auction '{auction.title}'."
            )

            messages.success(request, "Your bid has been placed successfully!")
            return redirect('auction_detail', pk=auction.pk)

    return render(request, 'auctions/auction_detail.html', {
        'auction': auction,
        'form': form,
        'error_messages': error_messages
    })


@login_required
def auction_create(request):
    if request.method == 'POST':
        form = AuctionItemForm(request.POST, request.FILES)
        if form.is_valid():
            auction_item = form.save(commit=False)
            auction_item.created_by = request.user
            auction_item.current_price = auction_item.starting_price
            auction_item.save()
            messages.success(request, 'Your auction has been created!')
            return redirect('auction_detail', pk=auction_item.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuctionItemForm()
    return render(request, 'auctions/auction_create.html', {'form': form})


@login_required
def search(request):
    search_query = request.GET.get('search', '')

    if search_query:
        results = AuctionItem.objects.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    else:
        # ordered by title
        results = AuctionItem.objects.all().order_by('title')

    return render(request, 'auctions/search.html', {'results': results, 'search_query': search_query})


@login_required
def add_to_watchlist(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)
    request.user.watchlist.add(auction)
    return redirect('auction_detail', pk=pk)


@login_required
def remove_from_watchlist(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)
    request.user.watchlist.remove(auction)
    return redirect('auction_detail', pk=pk)


def view_watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})


@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'auctions/notifications.html', {'notifications': user_notifications})


@login_required
def user_auctions(request):
    auctions = AuctionItem.objects.filter(created_by=request.user)
    return render(request, 'auctions/user_auctions.html', {'auctions': auctions})


def export_auctions(request, format):
    auctions = AuctionItem.objects.all()

    # Apply filters
    show_closed = request.GET.get('show_closed', 'off') == 'on'
    if not show_closed:
        auctions = auctions.filter(auction_end_date__gt=timezone.now())

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        auctions = auctions.filter(auction_end_date__gte=date_from)
    if date_to:
        auctions = auctions.filter(auction_end_date__lte=date_to)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        auctions = auctions.filter(current_price__gte=min_price)
    if max_price:
        auctions = auctions.filter(current_price__lte=max_price)

    show_with_image = request.GET.get('show_with_image', 'off') == 'on'
    if show_with_image:
        auctions = auctions.filter(image__isnull=False)

    sort_by = request.GET.get('sort_by')
    if sort_by == 'price':
        auctions = auctions.order_by('current_price')
    elif sort_by == '-price':
        auctions = auctions.order_by('-current_price')
    elif sort_by == 'date':
        auctions = auctions.order_by('auction_end_date')
    elif sort_by == '-date':
        auctions = auctions.order_by('-auction_end_date')

    if format == 'xml':
        root = ET.Element('Auctions')
        for auction in auctions:
            auction_elem = ET.SubElement(root, 'Auction')
            ET.SubElement(auction_elem, 'Title').text = auction.title
            ET.SubElement(auction_elem, 'Description').text = auction.description
            ET.SubElement(auction_elem, 'CurrentPrice').text = str(auction.current_price)
            ET.SubElement(auction_elem, 'EndDate').text = auction.auction_end_date.isoformat()

        tree = ET.ElementTree(root)
        response = HttpResponse(content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="auctions.xml"'
        tree.write(response, encoding='utf-8', xml_declaration=True)
        return response

    elif format == 'excel':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="auctions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Current Price', 'End Date'])
        for auction in auctions:
            writer.writerow([auction.title, auction.description, auction.current_price, auction.auction_end_date])

        return response

    else:
        return HttpResponse(status=400)


def api_auctions(request):
    format = request.GET.get('format', 'json')
    auctions = get_list_or_404(AuctionItem)

    if format == 'xml':
        root = ET.Element('Auctions')
        for auction in auctions:
            auction_elem = ET.SubElement(root, 'Auction')
            ET.SubElement(auction_elem, 'Title').text = auction.title
            ET.SubElement(auction_elem, 'Description').text = auction.description
            ET.SubElement(auction_elem, 'CurrentPrice').text = str(auction.current_price)
            ET.SubElement(auction_elem, 'EndDate').text = auction.auction_end_date.isoformat()

        tree = ET.ElementTree(root)
        response = HttpResponse(content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="auctions.xml"'
        tree.write(response, encoding='utf-8', xml_declaration=True)
        return response

    else:  # Default to JSON
        data = [
            {
                'title': auction.title,
                'description': auction.description,
                'current_price': auction.current_price,
                'end_date': auction.auction_end_date.isoformat()
            }
            for auction in auctions
        ]
        return JsonResponse(data, safe=False)
