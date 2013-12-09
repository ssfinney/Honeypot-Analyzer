class EntriesController < ApplicationController
  before_filter :authenticate_user!

  def index
    @entries = Entry.all
  end

  def new
    @log = Log.find(params[:log_id])
    @entry = Entry.new

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @entry }
    end
  end

  def create
    @log = Log.find(params[:log_id])
    @entry = @log.entries.new(params[:entry])

    respond_to do |format|
      if @entry.save
        format.html { redirect_to @entry, notice: 'Log entry was successfully created.' }
        format.json { render json: @entry, status: :created }
      else
        format.html { render action: "new" }
        format.json { render json: @entry.errors, status: :unprocessable_entity }
      end
    end
  end

  # POST: /users/<id>/logs/<id>/entries/create_many
  def create_many
    @log = Log.find(params[:log_id])
    
    entries = []
    params[:entries].length.times do |i| 
      entries << Entry.new(params[:entries][i])
    end
    Entry.import entries
  end

  def show
    @entry = Entry.find([params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @entry }
    end
  end

end

