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

  def show
    @entry = Entry.find([params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @entry }
    end
  end

end

